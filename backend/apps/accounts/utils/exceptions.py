class EmailSendError(Exception):
    """이메일 발송 관련 예외"""
    pass

class SMTPConfigError(EmailSendError):
    """SMTP 설정 오류"""
    pass

class NetworkError(EmailSendError):
    """네트워크 연결 오류"""
    pass