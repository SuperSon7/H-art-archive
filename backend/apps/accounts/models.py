from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수 입니다')
                
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_approved", True)
        return self.create_user(email, username, password, **extra_fields)
#TODO: need to add more fiedls for terms and privacy agreement
class User(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        ARTIST = 'ARTIST', '작가'
        COLLECTOR = 'COLLECTOR', '컬렉터'
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.COLLECTOR)
    
    is_approved = models.BooleanField(default=False) # 작가만 해당
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self):
        return f"[{self.user_type}] {self.username or self.email}"
    
    def get_following_list(self):
        return self.following.select_related('following')
    
    def get_following_count(self):
        return self.following.count()
    
    def is_following(self, artist):
        return self.following.filter(following=artist).exists()
    
    def get_wishlist(self):
        return self.wishlist.select_related('artwork')

    def get_wishlist_count(self):
        return self.wishlist.count()
    
    def get_unread_notifications(self):
        return self.notifications.filter(is_read=False)

    def get_unread_count(self):
        return self.notifications.filter(is_read=False).count()

    def mark_all_notifications_read(self):
        self.notifications.filter(is_read=False).update(is_read=True)
        