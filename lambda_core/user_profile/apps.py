from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserProfileConfig(AppConfig):
    name = 'lambda_core.user_profile'
    verbose_name = _('Lambda Core')
