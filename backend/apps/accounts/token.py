import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.core.cache import cache
import uuid
import logging
logger = logging.getLogger(__name__)

from apps.common.types import *

def generate_email_verification_token(uid : int, email : str) -> TokenStr:
    payload = {
        'user_id': uid,
        'email': email,
        'type': 'email_verification',
        'iat' : datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES),
        'jti': str(uuid.uuid4())
    }
    
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_email_verification_token(token : TokenStr) -> None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        jti = payload.get('jti')
        
        if not jti:
            raise ValueError("token does not contain JTI")
        
        if is_token_blacklisted(jti):
            raise ValueError("already used token")
        
        if payload.get('type') != 'email_verification':
            raise ValueError("wrong token category")
        
        if not payload.get('user_id') or not payload.get('email'):
            raise ValueError("token does not have essential info")
        
        logger.info(f"Sucess email token varification: {payload.get('email')}")
        return payload
    
    except jwt.ExpiredSignatureError:
        logger.info(f"token period expires")
        raise ValueError("Token expires")
    except jwt.InvalidTokenError:
        logger.warning(f"Invalid token")
        raise ValueError("Invalid token")
    except Exception as e:
        raise ValueError(f"An error occurred while processing the token: {str(e)}")
    
def add_token_to_blacklist(jti : str, exp_timestamp : float) -> None:
    """ 사용 토큰 블랙리스트

    Args:
        jti (str): 토큰에 대한 키 값
        exp_timestamp (float): 만료 시간
    """
    cache_key = f"blacklist_token:{jti}"
    ttl = int(exp_timestamp - datetime.now(timezone.utc).timestamp())
    
    if ttl > 0 : 
        cache.set(cache_key, "used", ttl)
        
def is_token_blacklisted(jti : str) -> bool:
    cache_key = f"blacklist_token:{jti}"
    return cache.get(cache_key) is not None