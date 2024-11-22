from django import forms
from django.utils.translation import ugettext_lazy as _

from lambda_core.widgets import ClearableFileInput


class ProfileForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'), required=True)
    last_name = forms.CharField(label=_('Last Name'), required=True)
    email = forms.CharField(label=_('Email'), required=True)
    avatar = forms.FileField(label=_('Avatar'), required=False, widget=ClearableFileInput)
