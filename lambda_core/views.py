from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.views import View
from django.utils.translation import ugettext_lazy as _

# noinspection PyPackageRequirements
from django.views.generic import ListView
from knox.views import LoginView as KnoxLoginView
import django_filters as filters
from lambda_theme_tailwindcss import widgets
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from lambda_core.filters import FilterSet

User = get_user_model()


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    # noinspection PyShadowingBuiltins
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class DataTableView(ListView):
    PAGINATOR_PER_PAGE = 25
    PAGINATOR_PAGE_LIMITS = [10, 25, 50, 100]
    PAGINATOR_PAGE_RANGE_LIMIT = 5

    PAGINATOR_PER_PAGE_KEY = 'limit'
    PAGINATOR_PAGE_KEY = 'page'
    PAGINATOR_SEARCH_KEY = 'search'

    headers = []
    filter_set = None
    template_name = 'datatable/base.html'

    def get_filter_set(self, *args, **kwargs):
        if self.filter_set:
            filter_set = self.filter_set(*args, **kwargs)
            return filter_set, filter_set.qs
        return None, kwargs.get('queryset', self.get_queryset())

    def get_paginate_by(self, queryset):
        return int(self.request.GET.get(self.PAGINATOR_PER_PAGE_KEY, self.PAGINATOR_PER_PAGE))

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        total = queryset.count()
        filter_set, object_list = self.get_filter_set(self.request.GET, queryset=queryset)
        context = super().get_context_data(object_list=object_list)

        paginator = context['paginator']
        object_list = context['object_list']
        page_obj = context['page_obj']

        index = page_obj.number - 1
        per_page = self.get_paginate_by(object_list)
        max_index = len(paginator.page_range)
        range_limit = self.PAGINATOR_PAGE_RANGE_LIMIT
        start_index = index - range_limit if index >= range_limit else 0
        end_index = index + range_limit if index <= max_index - range_limit else max_index

        context['total'] = total
        context['page_total'] = len(object_list)
        context['page_limits'] = self.PAGINATOR_PAGE_LIMITS
        context['per_page'] = per_page
        context['page'] = page_obj
        context['page_range'] = paginator.page_range[start_index:end_index]
        context['filter_set'] = filter_set
        context['headers'] = self.headers
        return context


class SettingsView(View):
    template_name = 'settings/base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# noinspection DuplicatedCode
class HijackFilterSet(FilterSet):
    username = filters.CharFilter(
        label=_("Username"),
        lookup_expr='icontains',
        widget=widgets.TextInput
    )
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

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


# noinspection PyMethodMayBeStatic
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('auth.view_user', raise_exception=True), name='dispatch')
class HijackUserListView(DataTableView):
    template_name = 'hijack/user_list.html'
    queryset = User.objects.all()
    filter_set = HijackFilterSet
