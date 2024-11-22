from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as ContribUserChangeForm
from django.utils.translation import ugettext_lazy as _

from allauth.account import forms as allauth

from lambda_theme_tailwindcss import widgets

__all__ = [
    'LoginForm',
    'SignupForm',
    'ChangePasswordForm',
    'AddEmailForm',
    'SetPasswordForm',
    'ResetPasswordForm',
    'ResetPasswordKeyForm',
    'UserChangeForm'
]


class UserChangeForm(ContribUserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = get_user_model()
        exclude = [
            'password',
            'last_login',
            'is_superuser',
            'groups',
            'user_permissions',
            'is_staff',
            'is_active',
            'date_joined',
        ]


class LoginForm(allauth.LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = widgets.TextInput({'autofocus': 'autofocus'})
        self.fields['password'].widget = widgets.PasswordInput(render_value=True)
        self.fields['remember'].widget = widgets.CheckboxInput()


class SignupForm(allauth.SignupForm):

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = widgets.TextInput()
        self.fields['password1'].widget = widgets.PasswordInput(render_value=True)
        if 'username' in self.fields:
            self.fields['username'].widget = widgets.TextInput()
        if 'password2' in self.fields:
            self.fields['password2'].widget = widgets.PasswordInput(render_value=True)


class ChangePasswordForm(allauth.ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].widget = widgets.PasswordInput()
        self.fields['password1'].widget = widgets.PasswordInput()
        self.fields['password2'].widget = widgets.PasswordInput()


class AddEmailForm(allauth.AddEmailForm):

    def __init__(self, user=None, *args, **kwargs):
        super(AddEmailForm, self).__init__(user, *args, **kwargs)
        self.fields['email'].widget = widgets.EmailInput()


class SetPasswordForm(allauth.SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = widgets.PasswordInput()
        self.fields['password2'].widget = widgets.PasswordInput()


class ResetPasswordForm(allauth.ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = widgets.EmailInput()


class ResetPasswordKeyForm(allauth.ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = widgets.PasswordInput()
        self.fields['password2'].widget = widgets.PasswordInput()
