import logging

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.apps.utils import IsSelf
from .serializers import ArtistProfileSerializer
class ArtistsProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing artists.
    Provides CRUD operations and additional features like following artists.
    """
    queryset = get_user_model().objects.filter(user_type='ARTIST')
    serializer_class = ArtistProfileSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    # mvp에서는 인증된 사용자만 접근 
    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'artist'):
            raise ValidationError("You already have an artist profile.")
        serializer.save(user=self.request.user)
    
    @action(detail=True,  methods=["post"], permission_classes=[IsAdminUser], url_path="approve")
    def approve_artist(self, request, pk=None)-> Response:
        """
        Approve an artist profile.
        Only accessible by admin users.
        """
        artist = self.get_object()
        if not artist.is_approved:
            artist.user.is_approved = True
            artist.user.save()
            return Response({"detail": "Artist approved successfully."}, status=status.HTTP_200_OK)
        raise ValidationError("Artist is already approved.")
    
    @action(detail=True,  methods=["post"], permission_classes=[IsAdminUser], url_path="reject")
    def reject_artist(self, request, pk=None)-> Response:
        """
        Reject an artist profile.
        Only accessible by admin users.
        """
        artist = self.get_object()
        if artist.is_approved:
            artist.user.is_approved = False
            artist.user.save()
            return Response({"detail": "Artist rejected successfully."}, status=status.HTTP_200_OK)
        raise ValidationError("Artist is not approved.")
