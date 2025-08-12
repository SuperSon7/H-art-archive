import os

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class S3ImageUploadSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255)
    content_type = serializers.CharField(max_length=50)
    
    def validate(self, attrs):
        filename = attrs.get('filename')
        content_type = attrs.get('content_type')
        
        if not filename or not content_type:
            raise serializers.ValidationError("Filename and content type are required")
        
        valid_content_types = {
            'image/jpeg': ['.jpg', '.jpeg'],
            'image/png': ['.png'],
            'image/gif': ['.gif'],
            'image/webp': ['.webp'],
        }
        if content_type not in valid_content_types:
            raise serializers.ValidationError("Invalid content type")
        
        # check content type against file extension
        file_ext = os.path.splitext(filename.lower())[1]
        if file_ext not in valid_content_types[content_type]:
            raise serializers.ValidationError("File extension doesn't match content type")
        
        return attrs