import logging

from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.artists.models import Artist
from apps.utils.permissions import IsSelf
from apps.utils.s3_presigner import create_presigned_url, s3_key_for_upload
from apps.utils.serializers import S3ImageUploadSerializer

from .serializers import ArtistAdminSerializer, ArtistProfileSerializer

logger = logging.getLogger(__name__)


# TODO 대표 이미지 presigned 설정
class ArtistProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing artists.
    Provides CRUD operations and additional features like following artists.
    """

    serializer_class = ArtistProfileSerializer

    def get_queryset(self):
        return (
            Artist.objects.filter(
                user__user_type="ARTIST",
            )
            .select_related("user")
            .prefetch_related("artworks")
        )

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSelf()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # TODO perform_create와 generate_main_image_url의 로직을 일치시킬지 결정
    # main_image 업데이트를 허용할 건지, 아니면 한 번만 생성 가능하게 할 건지
    def perform_create(self, serializer):
        if self.request.user.user_type != "ARTIST":
            raise ValidationError("Only artist can create main image.")
        serializer.save(user=self.request.user)

    def get_artist_for_me(self, user):
        try:
            artist = Artist.objects.get(user=user)
            return artist
        except Artist.DoesNotExist:
            raise NotFound("Artist not found")

    # TODO artwork와 연결
    # @action(detail=False, methods=["get"], url_path="me/main-image/from-artwork", url_name="main-image-select")
    # def get_artwork_for_main_image(self, request, pk=None) -> Response:
    #     """
    #     Get a list of artworks for the artist's main image selection.
    #     """
    #     artist = self.get_object()
    #     artworks = artist.artworks.all()
    #     # serializer = ArtworkSerializer(artworks, many=True)
    #     # return Response(serializer.data)

    #
    # @action(detail=False, methods=["put"], url_path="me/main-image/from-artwork", url_name="set-main-image-select")
    # def select_artwork_for_main_image(self, request, pk=None) -> Response:
    #     """
    #     Select an artwork for the artist's main image.
    #     """
    #     artist = self.get_object()
    #     artwork_id = request.data.get("artwork_id")
    #     if not artwork_id:
    #         raise ValidationError("artwork_id is required")
    #     # artwork = Artwork.objects.get(id=artwork_id)
    #     artwork = "TO_DO"
    #     artist.main_image_url = artwork.image_url
    #     artist.save(update_fields=["main_image_url"])
    #     return Response({"detail": "Main image selected successfully."})

    # TODO: mixin 활용 로직 검토
    @action(
        detail=False,
        methods=["post"],
        url_path="me/main-image/presigned",
        url_name="main-image-presigned",
    )
    def generate_main_image_url(self, request, pk=None) -> Response:
        """Generate a presigned URL for uploading a main image to S3

        Raises:
            NotFound: Artist not found

        Response:
            "upload_url": S3 presigned URL
            "s3_key": S3 key of image inside the bucket
        """
        artist = self.get_artist_for_me(request.user)

        serializer = S3ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bucket = getattr(settings, "AWS_S3_PROFILE_BUCKET", None)
        if not bucket:
            return Response(
                {"error": "AWS_S3_PROFILE_BUCKET not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        ext = serializer.validated_data["ext"]

        try:
            s3_key = s3_key_for_upload(
                category="profiles", object_id=artist.user.id, ext=ext, subdir="artist_main"
            )
        except Exception as e:
            logger.error(f"Failed to generate s3_key for {artist.user.id}: {str(e)}")
            raise ValidationError("Failed to generate s3_key")

        try:
            url, key = create_presigned_url(
                bucket=bucket,
                key=s3_key,
                content_type=serializer.validated_data["content_type"],
            )
        except ClientError as e:
            logger.error(f"AWS S3 error for artist {artist.id}: {e}")
            return Response(
                {"error": "S3 service error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.error(f"Unexpected error for artist {artist.id}: {e}")
            return Response(
                {"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"upload_url": url, "s3_key": key})

    # TODO: 키 저장 방식으로 변경, HeadObject 활용 필요
    @action(detail=False, methods=["post"], url_path="me/main-image", url_name="main-image")
    def save_main_image(self, request, pk=None) -> Response:
        """
        Save the main image presigned url to the artist's profile.
        """
        artist = self.get_artist_for_me(request.user)

        key = request.data.get("key")
        if not key:
            raise ValidationError("key is required")

        expected_prefix = f"profiles/{artist.user.id}/artist_main/"
        if not key.startswith(expected_prefix):
            raise ValidationError("Invalid S3 key")

        # TODO: 실제 업로드 여부 확인 필요

        url = request.data.get("url")

        artist.main_image_url = f"{url}/{key}"
        artist.save(update_fields=["main_image_url"])

        logger.info(f"Artist {artist.id} updated main image")
        return Response({"success": True})


# TODO 알림이나 로그, 통계, 일괄 승인로직 추가
class ArtistsAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ArtistAdminSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return (
            Artist.objects.filter(
                user__user_type="ARTIST",
            )
            .select_related("user")
            .prefetch_related("artworks")
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None) -> Response:
        """
        Approve an artist profile.
        Only accessible by admin users.
        """
        artist = self.get_object()
        if artist.is_approved:
            raise ValidationError("Artist is already approved.")
        artist.approval_status = Artist.ApprovalStatus.APPROVED
        artist.save()
        return Response({"detail": "Artist approved successfully."})

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None) -> Response:
        """
        Reject an artist profile.
        Only accessible by admin users.
        """
        artist = self.get_object()
        if artist.is_approved:
            artist.approval_status = Artist.ApprovalStatus.REJECTED
            artist.save()
            return Response({"detail": "Artist rejected successfully."})
        else:
            return Response({"detail": "Artist is already rejected."}, status=400)
