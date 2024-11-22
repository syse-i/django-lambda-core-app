from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LambdaCoreConfig(AppConfig):
    name = 'lambda_core'
    verbose_name = _('Lambda Core')
