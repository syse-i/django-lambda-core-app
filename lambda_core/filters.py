from django.utils.translation import ugettext_lazy as _

import django_filters as filters

from lambda_theme_tailwindcss import widgets


class FilterSet(filters.FilterSet):
    search = filters.CharFilter(
        label=_("Search"),
        widget=widgets.TextInput,
        method='search_filter'
    )

    @staticmethod
    def search_filter(queryset, name, value):
        try:
            return queryset.search({name: value})
        except AttributeError:
            return queryset
