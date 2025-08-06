from django.conf import settings
from django.core.cache import cache
from django.db import models
from parler.models import TranslatableModel, TranslatedFields

from apps.interactions.models import PurchaseInquiry


class Artist(TranslatableModel):
    translations = TranslatedFields(
        artist_name = models.CharField(max_length=150, db_index=True, help_text="작가명"),
        artist_note = models.TextField(blank=True, verbose_name="작가노트", help_text="작가 소개 및 작품 세계관")
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artist_profile'
    )
    
    # 작가용 대표 이미지, 기본 프로필과 별개
    profile_image = models.ImageField(upload_to='artists/profile/', blank=True, null=True, help_text="프로필 이미지")
    artwork_count = models.PositiveIntegerField(default=0, help_text="등록 작품 수")
    follower_count = models.PositiveBigIntegerField(default=0, help_text="팔로워 수")
    
    
    is_featured = models.BooleanField(
        default=False,
        help_text="추천 작가 여부"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "아티스트"
        verbose_name_plural = "아티스트들"
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['follower_count']),
            models.Index(fields=['is_featured'])
        ]

    
    
    def __str__(self):
        return self.safe_translation_getter('artist_name', any_language=True) or f"Artist #{self.pk}"
    
    @property
    def is_approved(self):
        """작가 승인 상태"""
        return self.user.user_type == 'ARTIST' and self.user.is_approved
    
    @property
    def is_currently_featured(self):
        if not self.is_featured:
            return False
        else : 
            return True
    
    def update_artwork_count(self):
        if hasattr(self, 'artworks'):
            self.artwork_count = self.artworks.filter(
                approval_status='approved',
                is_active=True
            ).count()
            self.save(update_fields=['artwork_count'])
    
            
    @classmethod
    def get_featured_artists(cls):
        cache_key = 'featured_artists'
        featured = cache.get(cache_key)
        
        if featured is None:
            featured = list(cls.objects.filter(
                is_featured=True,
                is_active=True,
                user__is_approved=True
            ).select_related('user'))
            cache.set(cache_key, featured, 60 * 15)
        
        return featured
    
    def get_followers_list(self):
        return self.followers.select_related('follower')

    def get_follower_count(self):
        return self.followers.count()
    
    def get_received_inquiries(self):
        return PurchaseInquiry.objects.filter(
            artwork__artist=self
        ).select_related('artwork', 'inquirer')

    def get_pending_inquiries_count(self):
        return PurchaseInquiry.objects.filter(
            artwork__artist=self,
            status='pending'
        ).count()