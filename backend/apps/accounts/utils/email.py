import logging
import smtplib
import socket
from datetime import datetime, time

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from rest_framework.exceptions import Throttled

from apps.common.types import TokenStr

from .exceptions import EmailSendError, NetworkError, SMTPConfigError

logger = logging.getLogger(__name__)

def send_verification_email(to_email : str, token : TokenStr):
    verify_url = f"{settings.FRONTEND_VERIFY_URL}?token={token}"
    subject = "이메일 인증을 완료해주세요"
    message = f"아래 링크를 클릭하여 이메일 인증을 완료해주세요:\n\n{verify_url}"
    html_content = f"""
    <p>아래 링크를 클릭하여 이메일 인증을 완료해주세요:</p>
    <p><a href="{verify_url}">이메일 인증 완료하기</a></p>
    """
    
    msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
    msg.attach_alternative(html_content,"text/html")
    
    try:
        msg.send(fail_silently=False)
        logger.info(f"이메일 발송 성공: {to_email}")
        return True


    except smtplib.SMTPAuthenticationError as e:
        logger.exception("SMTP 인증 오류")
        raise SMTPConfigError("이메일 서버 연결에 실패했습니다.") from e
        
    except smtplib.SMTPConnectError as e:
        logger.exception("SMTP 연결 실패")  
        raise SMTPConfigError("이메일 서버에 연결할 수 없습니다.") from e
    
    except (socket.timeout, socket.gaierror) as e:
        logger.exception("네트워크 연결 오류")
        raise NetworkError("이메일 서버에 연결할 수 없습니다.") from e
    
    except Exception as e:
        logger.exception("이메일 발송 실패")
        raise EmailSendError("이메일 발송 중 오류가 발생했습니다.") from e

def check_email_throttle(email: str, cooldown_seconds: int = 90, daily_limit: int = 500) -> None :
    """ 이메일 제한

    Args:
        email (str): 사용자 이메일
        cooldown_seconds (int, optional): 쿨다운 시간. Defaults to 90.
        daily_limit (int, optional): 일일 전송 횟수 제한. Defaults to 7.

    Raises:
        Throttled: _description_
        Throttled: _description_
    """
    cooldown_key = f"email_cooldown:{email}"
    if cache.get(cooldown_key):
        raise Throttled(detail="Please try again later.")

    cache.set(cooldown_key, "sent", timeout=cooldown_seconds)

    count_key = f"email_daily_count:{email}"
    current_count = cache.get(count_key)

    if current_count is not None and int(current_count) >= daily_limit:
        raise Throttled(detail="You can request authentication up to 5 times per day.")

    now = datetime.now()
    seconds_until_midnight = int((datetime.combine(now.date(), time.max) - now).total_seconds())

    if current_count is None:
        cache.set(count_key, 1, timeout=seconds_until_midnight)
    else:
        cache.incr(count_key)    