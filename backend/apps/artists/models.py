from django.db import models
from django.conf import settings
from parler.models import TranslatableModel, TranslatedFields

class Artist(TranslatableModel):
    translations = TranslatedFields(
        artist_name = models.CharField(max_length=150, db_index=True, help_text="작가명"),
        artist_note = models.TextField(blank=True, verbose_name="작가노트")
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artist_profile'
    )

    profile_image = models.ImageField(upload_to='artists/profile/', blank=True, null=True)
    artwork_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.safe_translation_getter('artist_name', any_language=True) or f"Artist #{self.pk}"
    
    @property
    def is_approved(self):
        """작가 승인 상태"""
        return self.user.user_type == 'ARTIST' and self.user.is_approved