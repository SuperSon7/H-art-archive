import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
import uuid
import logging
logger = logging.getLogger(__name__)

def generate_email_verification_token(uid, email):
    payload = {
        'user_id': uid,
        'email': email,
        'type': 'email_verification',
        'iat' : datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES),
        'jti': str(uuid.uuid4())
    }
    
    return jwt.encode(payload, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

def decode_email_verification_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        
        if payload.get('type') != 'email_verification':
            raise ValueError("잘못된 토큰 유형입니다.")
        
        if not payload.get('user_id') or not payload.get('email'):
            raise ValueError("토큰에 필수 정보가 없습니다.")
        
        logger.info(f"이메일 토큰 검증 성공: {payload.get('email')}")
        return payload
    
    except jwt.ExpiredSignatureError:
        logger.info(f"토큰 기간 만료")
        raise ValueError("토큰이 만료되었습니다.")
    except jwt.InvalidTokenError:
        logger.warning(f"유효하지 않은 토큰")
        raise ValueError("유효하지 않은 토큰입니다.")
    except Exception as e:
        raise ValueError(f"토큰 처리 중 오류가 발생했습니다: {str(e)}")