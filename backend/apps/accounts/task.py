@shared_task
def send_verification_email_task(email, token):
    send_verification_email(email, token)
