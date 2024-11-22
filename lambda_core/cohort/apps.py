from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TeamConfig(AppConfig):
    name = 'lambda_core.cohort'
    verbose_name = _('Lambda Core - Cohort')
