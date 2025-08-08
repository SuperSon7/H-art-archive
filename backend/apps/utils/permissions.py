from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()
class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        obj가 현재 로그인한 사용자와 같은지 판단하는 로직
        """
        if not request.user.is_authenticated:
            return False
        
        if isinstance(obj, get_user_model()):
            return obj == request.user
            
        if hasattr(obj, 'user'):
            user = getattr(obj, 'user', None)
            return user is not None and user == request.user
            
        return False