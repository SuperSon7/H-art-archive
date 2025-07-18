import smtplib
import socket
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging
from .exceptions import EmailSendError, SMTPConfigError, NetworkError
logger = logging.getLogger(__name__)

def send_verification_email(to_email, token):
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
    
    except (socket.timeout, socket.gaierror):
        logger.exception("네트워크 연결 오류")
        raise NetworkError("이메일 서버에 연결할 수 없습니다.") from e
    
    except Exception as e:
        logger.exception("이메일 발송 실패")
        raise EmailSendError("이메일 발송 중 오류가 발생했습니다.") from e

