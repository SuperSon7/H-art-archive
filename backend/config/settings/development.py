from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']


CORS_ALLOW_ALL_ORIGINS = True 

INSTALLED_APPS += [
    'django_extensions',
#     'debug_toolbar',  # 디버그 툴바 같은 다른 개발용 도구도 여기에 추가
]

DEFAULT_FROM_EMAIL = 'django.core.mail.backends.console.EmailBackend'