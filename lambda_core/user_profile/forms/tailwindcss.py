from django import forms
from lambda_theme_tailwindcss import widgets

from . import ProfileForm as BaseProfileForm

__all__ = ['ProfileForm']


class ProfileForm(BaseProfileForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget = widgets.TextInput()
        self.fields['last_name'].widget = widgets.TextInput()
        self.fields['email'].widget = widgets.EmailInput()
        self.fields['avatar'].widget = forms.FileInput()
