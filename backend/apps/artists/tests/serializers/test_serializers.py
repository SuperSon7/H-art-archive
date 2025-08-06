import pytest
from django.contrib.auth import get_user_model

from apps.artists.serializers import (
    ArtistProfileSerializer
)

User = get_user_model()

@pytest.mark.django_db
class TestArtistProfileSerializer:
    def test_artist_serializer_output_fields(self, artist):
        serializer = ArtistProfileSerializer(instance=artist)
        data = serializer.data
        
        assert 'artist_name' in data
        assert data['artist_name'] == "test artist"

        assert 'artist_note' in data
        assert data['artist_note'] == "This is test artist"

        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data