import logging

from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from apps.artists.models import Artist
from apps.accounts.models import User
from apps.utils.permissions import IsSelf
from .serializers import ArtistProfileSerializer, ArtistAdminSerializer
from apps.utils.serializers import S3ImageUploadSerializer
from apps.utils.s3_presigner import generate_presigned_url

logger = logging.getLogger(__name__)

class ArtistsProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing artists.
    Provides CRUD operations and additional features like following artists.
    """
    serializer_class = ArtistProfileSerializer
    # permission_classes = [IsAuthenticated, IsSelf]

    def get_queryset(self):
        return Artist.objects.filter(
            user__user_type='ARTIST',
        ).select_related('user').prefetch_related('artworks')
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSelf()]
        elif self.action in ['approve', 'reject']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'main_image'):
            raise ValidationError("You already have an main_image.")
        if self.request.user.user_type != 'ARTIST':
            raise ValidationError("Only artist can create main image.")
        serializer.save(user=self.request.user)
    
    def update(self, instance, validated_data):
        lang = self.context["request"].LANGUAGE_CODE
        instance.set_current_language(lang)
        instance.artist_name = validated_data.get("artist_name", instance.artist_name)
        instance.artist_note = validated_data.get("artist_note", instance.artist_note)
        if "profile_image" in validated_data:
            instance.profile_image = validated_data["profile_image"]
        instance.save()
        return instance
    
    def perform_update(self, serializer):
        print("✅ perform_update called with:", serializer.validated_data)
        serializer.save()
    
    @action(detail=True, methods=["post"], url_path="main-image")
    def generate_main_image_url(self, request, pk=None) -> Response:
        artist = self.get_object()
        if artist.user != request.user:
            raise PermissionDenied("You can only upload your own main image")

        serializer = S3ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            url, key = generate_presigned_url(
                user_id=request.user.id,
                filename=serializer.validated_data["filename"],
                content_type=serializer.validated_data["content_type"],
                folder="artist_main"  # 구분된 폴더 쓰기
            )
        except Exception as e:
            logger.error(f"Cover image presign error for artist {artist.id}: {e}")
            raise ValidationError("Failed to generate presigned URL")

        return Response({"upload_url": url, "s3_key": key})


    @action(detail=True, methods=["post"], url_path="main-image/save")
    def save_main_image(self, request, pk=None) -> Response:
        artist = self.get_object()
        if artist.user != request.user:
            raise PermissionDenied("You can only modify your own main image")
        
        key = request.data.get("key")
        if not key:
            raise ValidationError("key is required")

        expected_prefix = f"user_uploads/{request.user.id}/artist_main/"
        if not key.startswith(expected_prefix):
            raise ValidationError("Invalid S3 key")

        artist.main_image_url = f"https://{settings.AWS_S3_ARTWORK_BUCKET}.s3.amazonaws.com/{key}"
        artist.save(update_fields=["main_image_url"])

        logger.info(f"Artist {artist.id} updated main image")
        return Response({"success": True})
    

#TODO 알림이나 로그, 통계, 일괄 승인로직 추가
class ArtistsAdminViewSet(viewsets.ModelViewSet):
    
    serializer_class = ArtistAdminSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Artist.objects.filter(
            user__user_type='ARTIST',
        ).select_related('user').prefetch_related('artworks')
    
    @action(detail=True,  methods=["post"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None)-> Response:
        """
        Approve an artist profile.
        Only accessible by admin users.
        """
        artist = self.get_object()
        if artist.is_approved:
            raise ValidationError("Artist is already approved.")
        artist.user.approval_status = User.ApprovalStatus.APPROVED
        artist.user.save()
        return Response({"detail": "Artist approved successfully."})

    
    @action(detail=True,  methods=["post"], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None)-> Response:
        """
        Reject an artist profile.
        Only accessible by admin users.
        """
        artist = self.get_object()
        if artist.is_approved: 
            artist.user.approval_status = User.ApprovalStatus.REJECTED
            artist.user.save()
            return Response({"detail": "Artist rejected successfully."})
        else:
            return Response({"detail": "Artist is already rejected."}, status=400)