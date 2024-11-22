"""URL Configuration

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
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.translation import ugettext_lazy as _

import django_filters as filters
from notifications.signals import notify

from lambda_theme_tailwindcss import widgets

from lambda_core.filters import FilterSet
from lambda_core.urls import URLPatterns, path
from lambda_core.views import DataTableView


User = get_user_model()


class IndexView(View):

    def get(self, request):
        #notify.send(request.user, recipient=request.user, verb='you reached level 10')
        return render(request, 'index.html')


class Manager(models.Manager):

    def search(self, data):
        queryset = self.get_queryset()
        queryset = queryset.filter()
        return queryset


class DTFilter(FilterSet):
    first_name = filters.CharFilter(
        label=_("First Name"),
        lookup_expr='icontains',
        widget=widgets.TextInput
    )
    last_name = filters.CharFilter(
        label=_('Last Name'),
        lookup_expr='icontains',
        widget=widgets.TextInput
    )
    email = filters.CharFilter(
        label=_('Email'),
        lookup_expr='icontains',
        widget=widgets.TextInput
    )

    @staticmethod
    def search_filter(queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )


class DTView(DataTableView):
    headers = [
        {'text': 'ID', 'value': 'id'},
        {'text': 'First Name', 'value': 'first_name'},
        {'text': 'Last Name', 'value': 'last_name'},
        {'text': 'Email', 'value': 'email'},
    ]
    queryset = User.objects.all()
    filter_set = DTFilter


urlpatterns = URLPatterns(
    path('datatable/', DTView.as_view(), i18n=True),
    path('', login_required(IndexView.as_view()), i18n=True)
)
