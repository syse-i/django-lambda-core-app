from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import format_html, escape
from django.urls import reverse, NoReverseMatch


# @admin.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     date_hierarchy = 'action_time'
#
#     readonly_fields = [field.name for field in LogEntry._meta.get_fields()]
#
#     list_filter = [
#         'user',
#         'content_type',
#         'action_flag'
#     ]
#
#     search_fields = [
#         'object_repr',
#         'change_message'
#     ]
#
#     list_display = [
#         'action_time',
#         'user',
#         'content_type',
#         'object_link',
#         'action_flag',
#         'change_message',
#     ]
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_change_permission(self, request, obj=None):
#         return request.user.is_superuser and request.method != 'POST'
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def object_link(self, obj):
#         try:
#             if obj.action_flag == DELETION:
#                 link = obj.object_repr
#             else:
#                 ct = obj.content_type
#                 link = '<a href="{}">{}</a>'.format(
#                     reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
#                     escape(obj.object_repr)
#                 )
#             return format_html(link)
#         except NoReverseMatch:
#             return ""
#
#     object_link.allow_tags = True
#     object_link.admin_order_field = 'object_repr'
#     object_link.short_description = 'object'
#
#     def queryset(self, request):
#         return super(LogEntryAdmin, self).queryset(request).prefetch_related('content_type')
