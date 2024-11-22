from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _


class AbstractRole(TimeStampedModel):
    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s",
        related_query_name="%(app_label)s_%(class)ss",
    )
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.group.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        abstract = True


class AbstractCohort(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Users'),
        related_name="%(app_label)s_%(class)s",
        related_query_name="%(app_label)s_%(class)ss",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Cohort')
        verbose_name_plural = _('Cohorts')
        abstract = True
