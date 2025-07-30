from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from .models import User

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
            raise AuthenticationFailed('expired token')
        
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('invalid token')
        
        except User.DoesNotExist:
            raise AuthenticationFailed('user not found')
        
