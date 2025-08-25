import logging

from botocore.exceptions import ClientError
from django.conf import settings
from django.db import transaction
from django_filters import rest_framework as filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.artists.models import Artist
from apps.artworks.models import Artwork, ArtworkImage
from apps.utils.mixin import PresignedUploadMixin
from apps.utils.permissions import IsSelf
from apps.utils.serializers import ArtworkImageBatchSerializer, ConfirmBatchIn

# TODO: 상대 경로 수정 필요 컨테이너 환경 유의
from .filters import ArtworkFilter
from .serializers import (
    ArtworkAdminSerializer,
    ArtworkDetailSerializer,
    ArtworkListSerializer,
    MyArtworkSerializer,
)

logger = logging.getLogger(__name__)


class ArtworkPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class PublicArtworkViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArtworkListSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Artwork.objects.all()
    # TODO: 여러 필터 적용 기능 추가 필요
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ArtworkFilter
    pagination_class = ArtworkPagination

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("artist", "artist__user")
            .prefetch_related("images")
        )
        qs = qs.filter(approval_status=Artwork.ApprovalStatus.APPROVED)

        user = self.request.user
        if user.is_authenticated:
            qs = qs.filter(display_status=Artwork.DisplayStatus.PUBLIC)
        else:
            qs = qs.filter(display_status=Artwork.DisplayStatus.PUBLIC, is_featured=True)
        return qs

    # TODO: 조회수 증가 로직 추가 필요
    # @action(detail=True, methods=['post'])
    # def increment_view(self, request, pk=None):
    #     """조회수 증가 API"""
    #     artwork = self.get_object()
    #     artwork.increment_view_count()
    #     return Response({'view_count': artwork.view_count})

    def get_serializer_class(self):
        if getattr(self, "action", None) == "list":
            return ArtworkListSerializer
        if getattr(self, "action", None) == "retrieve":
            return ArtworkDetailSerializer
        # 스키마 생성 등 action이 None일 때의 안전망
        return self.serializer_class


class MyArtworkViewSet(PresignedUploadMixin, viewsets.ModelViewSet):
    serializer_class = MyArtworkSerializer
    permission_classes = [IsAuthenticated, IsSelf]
    pagination_class = ArtworkPagination

    def get_queryset(self):
        artist = self.get_artist_for_me(self.request.user)
        return Artwork.objects.filter(artist=artist)

    def perform_create(self, serializer):
        serializer.save(artist=self.get_artist_for_me(self.request.user))

    def get_artist_for_me(self, user):
        return Artist.objects.get(user=user)

    @action(
        detail=True,
        methods=["post"],
        url_path="images/presigned-batch",
        url_name="images-presigned-batch",
    )
    def presigned_batch(self, request, pk=None) -> Response:
        """
        Generate presigned URLs for multiple images.
        """
        artwork = self.get_object()
        if artwork.artist.user != request.user:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ArtworkImageBatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bucket = getattr(settings, "AWS_S3_ARTWORK_BUCKET", None)
        if not bucket:
            return Response(
                {"error": "AWS_S3_ARTWORK_BUCKET not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        items = []

        for f in serializer.validated_data["files"]:
            original_ext = f["ext"]
            key = self._build_s3_key(
                category="artworks",
                object_id=artwork.id,
                ext=original_ext,
                subdir="images",
            )
            url, k = self._get_presigned_url(
                bucket=bucket,
                key=key,
                content_type=f["content_type"],
            )
            items.append(
                {
                    "url": url,
                    "key": k,
                    "headers": {
                        "Content-Type": f["content_type"],
                        "Content-Length": str(f["size"]),
                    },
                }
            )

        return Response({"items": items}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="images/batch", url_name="images-batch")
    @transaction.atomic
    def confirm_batch(self, request, pk=None) -> Response:
        """
        Confirm multiple images.
        - Check for existence with HeadObject for each key
        - create ArtworkImage only for passed items
        - Specify cover if necessary
        """
        artwork = self.get_object()
        if artwork.artist.user != request.user:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ConfirmBatchIn(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        bucket = getattr(settings, "AWS_S3_ARTWORK_BUCKET", None)
        if not bucket:
            return Response(
                {"error": "AWS_S3_ARTWORK_BUCKET not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        created, failed = [], []
        s3 = self._get_s3_client()

        for item in data["items"]:
            key = item["key"]
            expected_prefix = f"artworks/{artwork.artist.user.id}/images/{artwork.id}/"

            if not key.startswith(expected_prefix):
                failed.append({"key": key, "reason": "invalid_prefix"})
                continue

            try:
                response = s3.head_object(Bucket=bucket, Key=key)
                file_size = response.get("ContentLength", 0)

                # 크기 제한 검증
                if file_size > settings.AWS_S3_MAX_FILE_SIZE:
                    failed.append({"key": key, "reason": "file_too_large"})
                    continue

            except ClientError as e:
                failed.append({"key": key, "reason": f"not_found: {str(e)}"})
                continue

            img = ArtworkImage.objects.create(
                artwork=artwork,
                key=key,
                alt_text=item.get("alt_text", ""),
                order=item.get("order", 0),
            )

            created.append({"key": key, "id": img.id, "file_size": file_size})

        cover = data.get("set_cover")
        if cover and any(c["key"] == cover for c in created):
            try:
                cov = ArtworkImage.objects.get(artwork=artwork, key=cover)
                artwork.cover_image = cov
                artwork.save(update_fields=["cover_image"])
            except ArtworkImage.DoesNotExist:
                logger.warning(f"Cover image not found: {cover}")

        return Response({"created": created, "failed": failed}, status=status.HTTP_200_OK)


class AdminArtworkViewSet(viewsets.ModelViewSet):
    serializer_class = ArtworkAdminSerializer
    permission_classes = [IsAdminUser]
    pagination_class = ArtworkPagination

    queryset = Artwork.objects.all()

    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ArtworkFilter

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("artist", "artist__user")
            .prefetch_related("images")
        )

    @action(detail=True, methods=["post"], url_path="approve", url_name="approve")
    def approve(self, request, pk=None) -> Response:
        artwork = self.get_object()
        artwork.approval_status = Artwork.ApprovalStatus.APPROVED
        artwork.save()
        return Response({"detail": "Artwork approved successfully."})

    @action(detail=True, methods=["post"], url_path="reject", url_name="reject")
    def reject(self, request, pk=None) -> Response:
        artwork = self.get_object()
        artwork.approval_status = Artwork.ApprovalStatus.REJECTED
        artwork.save()
        return Response({"detail": "Artwork rejected successfully."})

    @action(detail=True, methods=["post"], url_path="featured", url_name="set-featured")
    def set_featured(self, request, pk=None) -> Response:
        artwork = self.get_object()
        artwork.is_featured = True
        artwork.save()
        return Response({"detail": "Artwork set as featured successfully."})

    @action(detail=True, methods=["post"], url_path="unfeatured", url_name="set-unfeatured")
    def set_unfeatured(self, request, pk=None) -> Response:
        artwork = self.get_object()
        artwork.is_featured = False
        artwork.save()
        return Response({"detail": "Artwork set as unfeatured successfully."})

    # TODO: 강제 삭제, 일괄 승인/거부 로직 추가
