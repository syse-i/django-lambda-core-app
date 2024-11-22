import os

from lambda_config.settings import production
from lambda_core.settings import base

__all__ = ['Settings']


# noinspection PyPep8Naming
class Settings(base.Settings, production.Settings):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'storages',
        ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', 5432),
        }
    }

    # Django Storages
    # https://django-storages.readthedocs.io/en/latest/index.html

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = 's3-us-west-1.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    AWS_DEFAULT_ACL = 'public-read'

    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'lambda_core.storages.MediaStorage'

    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

    # django-sendgrid-v5
    # https://github.com/sklarsa/django-sendgrid-v5

    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

    # Maintenance Mode
    # https://github.com/fabiocaccamo/django-maintenance-mode

    # if True authenticated users will not see the maintenance-mode page
    MAINTENANCE_MODE_IGNORE_AUTHENTICATED_USER = False
