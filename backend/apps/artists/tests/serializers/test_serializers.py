import pytest
from django.contrib.auth import get_user_model

from apps.artists.serializers import ArtistProfileSerializer

User = get_user_model()

@pytest.mark.django_db
class TestArtistProfileSerializer:
    def test_artist_serializer_output_fields(self, artist):
        serializer = ArtistProfileSerializer(instance=artist)
        data = serializer.data
        
        assert 'translations' in data
        assert 'ko' in data['translations']
        t = data['translations']['ko']
        
        assert t['artist_name'] == "test artist"
        assert t['artist_note'] == "This is test artist"

        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data