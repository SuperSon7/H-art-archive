from rest_framework import serializers
from .models import Artist

class ArtistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [
            'id', 'artist_name', 'artist_note', 'profile_image',
            'artwork_count', 'follower_count', 'is_featured', 'is_approved',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'artwork_count', 'follower_count', 'is_featured', 
            'is_approved', 'created_at', 'updated_at'
        ]
        
        def get_isapproved(self, obj):
            """dedicated getter method to check if the artist is approved"""
            return getattr(obj.user, 'is_approved', False)