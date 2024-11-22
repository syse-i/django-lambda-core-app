"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import List

from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.conf.urls.static import static
from django.views.defaults import page_not_found

# noinspection PyPackageRequirements
from knox import views as knox_views
import lambda_url
import debug_toolbar

from .user_profile.views import ProfileView
from .views import HijackUserListView, LoginView

path = lambda_url.path

__all__ = [
    'URLPatterns',
    'path'
]


def trigger_error(request):
    return 1 / 0  # division_by_zero


class URLPatterns(lambda_url.URLPatterns):
    urls = [
        path('i18n/', include('django.conf.urls.i18n')),
        path('hijack/', include('hijack.urls', namespace='hijack')),
        path('admin/', admin.site.urls, i18n=True),
        # Third party routes
        path('notifications/', include('notifications.urls', namespace='notifications'), i18n=True),
        path('accounts/', include('allauth.urls'), i18n=True),
        # Our Routes
        path('accounts/profile/', ProfileView.as_view(), name='profile', i18n=True),
        path('login_as/', HijackUserListView.as_view(), name='login_as', i18n=True),
        # API
        path('api/', include('lambda_core.api')),
        # Knox REST auth
        # path('api-auth/', include('rest_framework.urls')),
        path('api/login/', LoginView.as_view(), name='knox_login'),
        path('api/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
        path('api/logout-all/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    ]

    def __new__(cls, *urls: List[path], **kwargs):
        if settings.DEBUG:
            cls.urls.append(path('__debug__/', include(debug_toolbar.urls)))
        if settings.DEBUG and settings.SENTRY_SDK_DSN:
            cls.urls.append(path('sentry-debug/', trigger_error))
        if not settings.ACCOUNT_SIGNUP_ENABLE:
            params = {'exception': Exception()}
            cls.urls.append(path('accounts/signup/', page_not_found, kwargs=params, i18n=True))

        urlpatterns = super(URLPatterns, cls).__new__(cls, *urls, **kwargs)
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        return urlpatterns
