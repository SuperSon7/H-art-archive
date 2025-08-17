import logging

from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.artists.models import Artist
from apps.artworks.models import Artwork
from apps.utils.permissions import IsSelf

from .filters import ArtworkFilter
from .serializers import ArtworkSerializer

logger = logging.getLogger(__name__)


class MyArtworkViewSet(viewsets.ModelViewSet):
    serializer_class = ArtworkSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    def get_queryset(self):
        artist = self.get_artist_for_me(self.request.user)
        return Artwork.objects.filter(artist=artist)

    def perform_create(self, serializer):
        serializer.save(artist=self.get_artist_for_me(self.request.user))

    def get_artist_for_me(self, user):
        return Artist.objects.get(user=user)


class PublicArtworkViewset(ReadOnlyModelViewSet):
    serializer_class = ArtworkSerializer
    permission_classes = [IsAuthenticated]
    queryset = Artwork.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ArtworkFilter

    def get(self, request):
        return Response(self.queryset.all(), status=status.HTTP_200_OK)


class AdminArtworkViewSet(viewsets.ModelViewSet):
    serializer_class = ArtworkSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Artwork.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
