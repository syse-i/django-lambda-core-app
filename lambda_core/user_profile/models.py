from os import path

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.core.signing import Signer
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _


def add_default_profile_permissions(sender, instance, created, **kwargs):
    current_codename = None
    try:
        user = instance
        permissions = ['change_own_userprofile']
        for codename in permissions:
            current_codename = codename
            current_permission = Permission.objects.get(codename=codename)
            user.user_permissions.add(current_permission)
    except Permission.DoesNotExist:
        pass
        #print('Cannot assign the permission {}'.format(current_codename))


def user_directory_path(instance, filename):
    name, ext = path.splitext(filename)
    signer = Signer()
    value = signer.sign(filename).split(":")
    return "avatar/{}{}".format(value[1], ext)


def create_user_profile(sender, instance, created, **kwargs):
    return UserProfile.objects.get_or_create(user=instance)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        permissions = [
            ('change_own_userprofile', _('Can change his own user profile'))
        ]


# Todo: do this post_save actions in view instead
post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
post_save.connect(add_default_profile_permissions, sender=settings.AUTH_USER_MODEL)
