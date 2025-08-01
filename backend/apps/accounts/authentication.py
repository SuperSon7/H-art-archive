import logging

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import User

logger = logging.getLogger(__name__)
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        
        try:   
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            user = User.objects.get(id=payload['user_id'])
            
            return (user, token)
        
        except jwt.ExpiredSignatureError:
            logger.warning("Expired JWT token used")
            raise AuthenticationFailed('Token expired')
        
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token used")
            raise AuthenticationFailed('Invalid token')
        
        except User.DoesNotExist:
            logger.warning(f"JWT token for non-existent user: {payload.get('user_id')}")
            raise AuthenticationFailed('User not found')
        
