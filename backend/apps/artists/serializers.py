from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer

from .models import Artist


class ArtistProfileSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Artist)

    class Meta:
        model = Artist
        fields = [
            'id', 'translations', 'main_image', 'artwork_count', 
            'follower_count', 'is_featured', 'approval_status',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'artwork_count', 'follower_count', 'is_featured', 
            'approval_status', 'created_at', 'updated_at'
        ]
        

    # def update(self, instance, validated_data):
    #     lang = translation.get_language()
    #     instance.set_current_language(lang)
    #     instance.artist_name = validated_data.get("artist_name", instance.artist_name)
    #     instance.artist_note = validated_data.get("artist_note", instance.artist_note)
    #     if "profile_image" in validated_data:
    #         instance.profile_image = validated_data["profile_image"]
    #     instance.save()
    #     return instance
    
    # def get_artist_name(self, obj):
    #     return obj.safe_translation_getter('artist_name', language_code=self._get_language())

    # def get_artist_note(self, obj):
    #     return obj.safe_translation_getter('artist_note', language_code=self._get_language())

    # def _get_language(self):
    #     request = self.context.get('request')
    #     return getattr(request, 'LANGUAGE_CODE', 'en') 

class ArtistAdminSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Artist)

    class Meta:
        model = Artist
        fields = [
            'id', 'translations', 'main_image', 'approval_status',
            'artwork_count', 'follower_count', 'is_featured', 
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'artwork_count', 'follower_count', 'is_featured', 
            'is_approved', 'created_at', 'updated_at'
        ]