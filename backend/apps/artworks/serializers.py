from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers

from .models import Artwork


class ArtworkListSerializer(TranslatableModelSerializer):
    title = serializers.SerializerMethodField()
    artist_name = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Artwork
        fields = [
            "id",
            "title",
            "price_krw",
            "price_usd",
            "artist_name",
            "thumbnail_url",
            "sale_status",
            "display_status",
            "like_count",
            "view_count",
            "is_featured",
        ]
        read_only_fields = [
            "id",
            "view_count",
            "like_count",
            "is_featured",
        ]

    def get_title(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def get_artist_name(self, obj):
        getter = getattr(obj.artist, "safe_translation_getter", None)
        if callable(getter):
            return getter("artist_name", any_language=True)
        return getattr(obj.artist, "name", None)

    # TODO: 썸네일 이미지 추가 필요
    # def get_thumbnail_url(self, obj):
    #     return obj.primary_image.image.url


class ArtworkDetailSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Artwork)
    artist_name = serializers.SerializerMethodField()

    class Meta:
        model = Artwork
        fields = [
            "id",
            "translations",
            "year_created",
            "price_krw",
            "price_usd",
            "materials",
            "width",
            "height",
            "depth",
            "category",
            "sale_status",
            "display_status",
            "view_count",
            "like_count",
            "is_featured",
            "artist_name",
        ]
        read_only_fields = [
            "id",
            "view_count",
            "like_count",
            "is_featured",
            "artist_name",
        ]


class MyArtworkSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Artwork)

    class Meta:
        model = Artwork
        fields = [
            "id",
            "translations",
            "year_created",
            "price_krw",
            "price_usd",
            "materials",
            "width",
            "height",
            "depth",
            "dimension_unit",
            "category",
            "status",
            "copyright_agreed",
            "license_agreed",
            "view_count",
            "like_count",
            "is_featured",
            "featured_at",
            "is_deleted",
            "deleted_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "view_count",
            "like_count",
            "copyright_agreed",
            "license_agreed",
            "is_featured",
            "featured_at",
            "is_deleted",
            "deleted_at",
            "created_at",
            "updated_at",
        ]


class ArtworkAdminSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Artwork)

    class Meta:
        model = Artwork
        fields = [
            "id",
            "translations",
            "year_created",
            "price_krw",
            "price_usd",
            "materials",
            "width",
            "height",
            "depth",
            "dimension_unit",
            "category",
            "status",
            "copyright_agreed",
            "license_agreed",
            "view_count",
            "like_count",
            "is_featured",
            "featured_at",
            "is_deleted",
            "deleted_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "view_count",
            "like_count",
            "featured_at",
            "is_deleted",
            "deleted_at",
            "created_at",
            "updated_at",
        ]
