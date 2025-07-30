from rest_framework import serializers
from django.contrib.auth import get_user_model
from .token import decode_email_verification_token
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'user_type', 'is_active', 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
class SignUpSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    agree_terms = serializers.BooleanField()
    agree_privacy = serializers.BooleanField()
    user_type = serializers.ChoiceField(choices=['artist', 'collector'])
    
    def validate_email(self, val):
        if User.objects.filter(email=val).exists():
            raise serializers.ValidationError("이미 존재하는 이메일입니다.")
        return val

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")            
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        
        user = User.objects.create_user(**validated_data)
        return user

class SendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, attrs):
        email = attrs['email']
        try:
            user = User.objects.get(email=email)
            attrs['uid'] = str(user.pk) 
            return attrs
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "존재하지 않는 이메일입니다."})
        
class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
    
    def validate(self, attrs):
        try:
            payload = decode_email_verification_token(attrs['token'])
            attrs['payload'] = payload
            return attrs
        except ValueError as e:
            raise serializers.ValidationError({"token": str(e)})
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    pasword = serializers.CharField(write_only=True, min_length=8)
    
    
class ProfileImageUploadSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255)
    content_type = serializers.CharField(max_length=50)
    
    def validate(self, attrs):
        filename = attrs.get('filename')
        content_type = attrs.get('content_type')
        
        if not filename or not content_type:
            raise serializers.ValidationError("Filename and content type are required")
        
        
        valid_content_types = [
            'image/jpeg',
            'image/png',
            'image/gif',
            'image/webp',
        ]
        if content_type not in valid_content_types:
            raise serializers.ValidationError("Invalid content type")
        
        return attrs

class SocialLoginSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    provider = serializers.ChoiceField(choices=["google", "naver"])
    redirct_uri = serializers.ChoiceField(required=False)