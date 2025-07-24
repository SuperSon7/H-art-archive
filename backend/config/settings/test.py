from .base import *

DEBUG = False
# ALLOWED_HOSTS = ['*']

# CORS_ALLOW_ALL_ORIGINS = True 

# INSTALLED_APPS += [
#     'django_extensions',
# #     'debug_toolbar',  # 디버그 툴바 같은 다른 개발용 도구도 여기에 추가
# ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# 비밀번호 해시 속도 향상
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]


DEFAULT_FROM_EMAIL = 'django.core.mail.backends.console.EmailBackend'