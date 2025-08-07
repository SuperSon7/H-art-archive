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

from apps.artists.models import Artist
from backend.apps.utils import IsSelf
from .serializers import ArtistProfileSerializer
class ArtistsProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing artists.
    Provides CRUD operations and additional features like following artists.
    """
    serializer_class = ArtistProfileSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    def get_queryset(self):
        return Artist.objects.filter(
            user__user_type='ARTIST',
        ).select_related('user').prefetch_related('artworks')
    # mvp에서는 인증된 사용자만 접근 
    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'artist_profile'):
            raise ValidationError("You already have an artist profile.")
        if self.request.user.user_type != 'ARTIST':
            raise ValidationError("Only artist users can create artist profiles.")
        serializer.save(user=self.request.user)
    
    @action(detail=True,  methods=["post"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None)-> Response:
        """
        Approve an artist profile.
        Only accessible by admin users.
        """
        artist = self.get_object()
        if artist.is_approved:
            raise ValidationError("Artist is already approved.")
        artist.user.is_approved = True
        artist.user.save()
        return Response({"detail": "Artist approved successfully."})

    
    @action(detail=True,  methods=["post"], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None)-> Response:
        """
        Reject an artist profile.
        Only accessible by admin users.
        """
        artist = self.get_object()
        if not artist.is_approved:
            raise ValidationError("Artist is not approved.")
        artist.user.is_approved = False
        artist.user.save()
        return Response({"detail": "Artist rejected successfully."})
