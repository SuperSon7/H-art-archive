import logging

from django.conf import settings
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.artists.models import Artist
from apps.artworks.models import Artwork
from apps.utils.mixin import PresignedUploadMixin
from apps.utils.permissions import IsSelf
from apps.utils.serializers import S3ImageUploadSerializer

# TODO: 상대 경로 수정 필요 컨테이너 환경 유의
from .filters import ArtworkFilter
from .serializers import (
    AdminArtworkSerializer,
    ArtworkDetailSerializer,
    ArtworkListSerializer,
    MyArtworkSerializer,
)

logger = logging.getLogger(__name__)


class ArtworkPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class PublicArtworkViewset(ReadOnlyModelViewSet):
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
        user = self.request.user
        if user.is_authenticated:
            qs = qs.filter(~Q(display_status=Artwork.DisplayStatus.HIDDEN))
        else:
            qs = qs.filter(is_featured=True)
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return ArtworkListSerializer
        return ArtworkDetailSerializer


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

    @action(detail=True, methods=["post"], url_path="images/presigned", url_name="images-presigned")
    def generate_image_url(self, request, pk=None) -> Response:
        """
        Generate a presigned URL for an image upload.

        Returns:
            Response: A dictionary containing the presigned URL and the S3 key.
        """
        artwork = self.get_object()

        serializer = S3ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bucket = getattr(settings, "AWS_S3_ARTWORK_BUCKET", None)
        if not bucket:
            return Response(
                {"error": "AWS_S3_ARTWORK_BUCKET not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        key = self._build_s3_key(
            category="artworks",
            object_id=artwork.id,
            ext=serializer.validated_data["ext"],
            subdir="images",
        )

        url, k = self.get_presigned_url(
            bucket=bucket,
            key=key,
            content_type=serializer.validated_data["content_type"],
        )

        return Response({"url": url, "key": k}, status=status.HTTP_200_OK)

    # TODO: URL 저장 로직 추가


class AdminArtworkViewSet(viewsets.ModelViewSet):
    serializer_class = AdminArtworkSerializer
    permission_classes = [IsAdminUser]
    pagination_class = ArtworkPagination

    def get_queryset(self):
        return Artwork.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
