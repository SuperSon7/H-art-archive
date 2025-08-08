from rest_framework import serializers
from .models import Artist
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

class ArtistProfileSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Artist)

    class Meta:
        model = Artist
        fields = [
            'id', 'translations', 'main_image',
            'artwork_count', 'follower_count', 'is_featured', 'is_approved',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'artwork_count', 'follower_count', 'is_featured', 
            'is_approved', 'created_at', 'updated_at'
        ]
        
        
    def get_artist_name(self, obj):
        return obj.safe_translation_getter('artist_name', language_code=self._get_language())

    def get_artist_note(self, obj):
        return obj.safe_translation_getter('artist_note', language_code=self._get_language())

    def _get_language(self):
        request = self.context.get('request')
        return getattr(request, 'LANGUAGE_CODE', 'en') 

class ArtistAdminSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Artist)

    class Meta:
        model = Artist
        fields = [
            'id', 'translations', 'main_image',
            'artwork_count', 'follower_count', 'is_featured', 'is_approved',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'artwork_count', 'follower_count', 'is_featured', 
            'is_approved', 'created_at', 'updated_at'
        ]