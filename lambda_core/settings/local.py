import os

from lambda_config.settings import local
from lambda_core.settings import base

__all__ = ['Settings']


class Settings(base.Settings, local.Settings):

    AUTH_PASSWORD_VALIDATORS = []

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    INTERNAL_IPS = [
        '127.0.0.1',
    ]

    EMAIL_HOST = '127.0.0.1'
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False

    SHELL_PLUS = "ipython"
    SHELL_PLUS_PRINT_SQL = True
