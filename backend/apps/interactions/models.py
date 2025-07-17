from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='following'
    )
    following = models.ForeignKey(
        'artists.Artist', 
        on_delete=models.CASCADE, 
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        db_table = 'interactions_follow'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.artist_name}"


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='wishlist'
    )
    artwork = models.ForeignKey(
        'artworks.Artwork', 
        on_delete=models.CASCADE, 
        related_name='wishlisted_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'artwork')
        db_table = 'interactions_wishlist'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} wishlisted {self.artwork.title}"
    
    
class PurchaseInquiry(models.Model):

    STATUS_CHOICES = [
        ('pending', '대기 중'),
        ('responded', '답변 완료'),
        ('completed', '구매 완료'),
        ('cancelled', '취소됨'),
    ]
    
    inquirer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='purchase_inquiries'
    )
    artwork = models.ForeignKey(
        'artworks.Artwork', 
        on_delete=models.CASCADE, 
        related_name='purchase_inquiries'
    )
    message = models.TextField(verbose_name="문의 내용")
    contact_phone = models.CharField(
        max_length=20, 
        validators=[RegexValidator(
            regex=r'^010-\d{4}-\d{4}$',
            message='올바른 전화번호 형식이 아닙니다. (010-XXXX-XXXX)'
        )],
        verbose_name="연락처"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    artist_response = models.TextField(blank=True, null=True, verbose_name="작가 답변")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'interactions_purchase_inquiry'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.inquirer.username} - {self.artwork.title}"
    
    def save(self, *args, **kwargs):
        if self.status == 'responded' and not self.responded_at:
            self.responded_at = timezone.now()
        super().save(*args, **kwargs)
        
        
class Notification(models.Model):
    
    TYPE_CHOICES = [
        ('follow', '팔로우'),
        ('artwork_upload', '작품 업로드'),
        ('purchase_inquiry', '구매 문의'),
        ('inquiry_response', '문의 답변'),
        ('like', '좋아요'),
        ('comment', '댓글'),
        ('system', '시스템 알림'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_notifications',
        blank=True, 
        null=True
    )
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    # 관련 객체 참조 (Generic Foreign Key 대신 구체적인 FK 사용)
    related_artwork = models.ForeignKey(
        'artworks.Artwork', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    related_artist = models.ForeignKey(
        'artists.Artist', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    related_inquiry = models.ForeignKey(
        PurchaseInquiry, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    
    class Meta:
        db_table = 'interactions_notification'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['recipient', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        """알림을 읽음으로 표시"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
