from celery import shared_task

from apps.common.types import *

from .utils.email import send_verification_email


@shared_task(bind=True, default_retry_delay=60)
def send_verification_email_task(self, email : str, token : TokenStr) -> None:
    try:
        print(f"[CELERY TASK] Sending email to {email} with token={token}")
        send_verification_email(email, token)
    except Exception as exc:
        self.retry(exc=exc)
