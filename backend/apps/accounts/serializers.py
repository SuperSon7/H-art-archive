from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=150)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password  = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    agree_terms = serializers.BooleanField()
    agree_privacy = serializers.BooleanField()

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