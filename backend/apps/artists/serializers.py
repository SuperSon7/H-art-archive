from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer

from .models import Artist


class ArtistProfileSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Artist)

    class Meta:
        model = Artist
        fields = [
            "id",
            "translations",
            "main_image_url",
            "artwork_count",
            "follower_count",
            "is_featured",
            "approval_status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "main_image_url",
            "artwork_count",
            "follower_count",
            "is_featured",
            "approval_status",
            "created_at",
            "updated_at",
        ]


class ArtistAdminSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Artist)

    class Meta:
        model = Artist
        fields = [
            "id",
            "translations",
            "main_image_url",
            "approval_status",
            "artwork_count",
            "follower_count",
            "is_featured",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "artwork_count",
            "follower_count",
            "is_featured",
            "is_approved",
            "created_at",
            "updated_at",
        ]
