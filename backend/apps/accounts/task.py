from celery import shared_task
from .utils.email import send_verification_email
from apps.common.types import *

@shared_task(bind=True, default_retry_delay=60)
def send_verification_email_task(self, email : str, token : TokenStr) -> None:
    try:
        send_verification_email(email, token)
    except Exception as exc:
        self.retry(exc=exc)
