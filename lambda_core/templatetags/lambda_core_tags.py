# noinspection PyUnresolvedReferences
from urllib.parse import urljoin, urlencode

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lambda_theme import template
from lambda_theme.template.components import Link, Slot
from lambda_theme.template.filters import is_checkbox
from lambda_theme.template.tags import form_errors, form_field, form_fields, \
    formset_render, message, messages

from lambda_theme_tailwindcss.template.components import Alert, Button, Breadcrumb, Card, Dropdown, Label
from lambda_theme_tailwindcss.template.tags import badge, breadcrumb_item, dropdown_item, dropdown_item_divider

User = get_user_model()

register = template.Library()

# Components

register.tag('slot', Slot)
register.tag('alert', Alert)
register.tag('link', Link)
register.tag('button', Button)
register.tag('breadcrumb', Breadcrumb)
register.tag('card', Card)
register.tag('dropdown', Dropdown)
register.tag('label', Label)

# Inclusion Tags


def form_render(*forms, method='POST', submit_label=_("Submit"), **attributes):
    context = template.TagContext(attributes)
    context['forms'] = forms
    context['method'] = method
    context['submit_label'] = submit_label
    return context.flatten()


# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/form_base.html')(form_render)
# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/form_errors.html')(form_errors)
# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/form_field.html')(form_field)
# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/form_fields.html')(form_fields)
# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/formset_base.html')(formset_render)
# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/message.html')(message)
# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/messages.html', takes_context=True)(messages)
# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/badge.html')(badge)
# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/breadcrumb_item.html')(breadcrumb_item)
# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/dropdown_item.html')(dropdown_item)
# noinspection PyUnresolvedReferences
register.inclusion_tag('@tags/dropdown_item_divider.html')(dropdown_item_divider)


# noinspection PyUnresolvedReferences
@register.inclusion_tag('@tags/no_content.html')
def no_content(width="240px", **attributes):
    context = template.TagContext(attributes)
    context['width'] = width
    return context.flatten()


# noinspection PyUnresolvedReferences
@register.inclusion_tag('@tags/logo.html', takes_context=True)
def logo(context, title=None, url=None, **attributes):
    context = template.TagContext(attributes, initial=context)
    context['title'] = title
    context['url'] = reverse(url) if url else '/'
    return context.flatten()


# noinspection PyUnresolvedReferences
@register.inclusion_tag('@tags/language_selector.html')
def language_selector(**attributes):
    context = template.TagContext(attributes)
    return context.flatten()


# noinspection PyUnresolvedReferences
@register.inclusion_tag('@tags/user_profile.html', takes_context=True)
def user_profile(context, orientation='right', **attributes):
    context = template.TagContext(attributes, initial=context)
    context['orientation'] = orientation
    return context.flatten()


# noinspection PyUnresolvedReferences
@register.inclusion_tag('@tags/user_fullname.html', takes_context=True)
def user_fullname(context, user=None, truncatechars=25, **attributes):
    context = template.TagContext(attributes, initial=context)
    context.update({
        'user': user if user else context['request'].user,
        'truncate_length': truncatechars,
    })
    return context.flatten()


# noinspection PyUnresolvedReferences
@register.inclusion_tag('@tags/user_avatar.html', takes_context=True)
def user_avatar(context, user=None, width=35, height=35, **attributes):
    context = template.TagContext(attributes, initial=context)
    context.update({
        'user': user if user else context['request'].user,
        'width': width,
        'height': height,
    })
    return context.flatten()


# noinspection PyUnresolvedReferences
@register.inclusion_tag('@tags/pagination.html', takes_context=True)
def pagination(context, page_obj=None, page_range=None, **attributes):
    page_obj = page_obj if page_obj else context.get('page')
    page_range = page_range if page_range else context.get('page_range', 0)
    context = template.TagContext(attributes, initial=context)
    context.update({
        'page_obj': page_obj,
        'page_range': page_range,
    })
    return context.flatten()


# noinspection PyUnresolvedReferences
@register.inclusion_tag('@tags/pagination_filters.html', takes_context=True)
def pagination_filters(context, per_page=None, **attributes):
    search = context.get('search')
    page_limits = context.get('page_limits', [])
    per_page = per_page if per_page else context.get('per_page', 20)
    context = template.TagContext(attributes, initial=context)
    context.update({
        'search': search,
        'page_limits': page_limits,
        'per_page': per_page
    })
    return context.flatten()


@register.simple_tag(takes_context=True)
def relative_url(context, **kwargs):
    request = context['request']
    data = request.GET.copy()
    # Important: since data(QueryDict) update method doesnt
    # overwrite the dict, manually setting the key value
    # is the only way to workaround this.
    for (key, value) in kwargs.items():
        data[key] = value
    url_params = data.urlencode()
    base_url = request.path
    return f'{base_url}?{url_params}'if url_params else base_url


def get_settings(attr):
    return getattr(settings, attr)


register.simple_tag(get_settings, name='settings')


def merge_args(args):
    return "".join([str(x) for x in args])


@register.simple_tag(takes_context=True)
def absolute_url(context, *args):
    request = context['request']
    return request.build_absolute_uri(merge_args(args))


# Filters

register.filter(is_checkbox)


@register.filter
def attribute(obj, key, default=None):
    return getattr(obj, key, default)


# noinspection PyPep8Naming
@register.filter
def hijack_user(request):
    try:
        hijack_history = request.session.get('hijack_history', [])
        return User.objects.get(pk=hijack_history[-1])
    except (AttributeError, IndexError, User.DoesNotExist):
        pass
