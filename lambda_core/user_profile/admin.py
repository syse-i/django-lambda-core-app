from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    raw_id_fields = ('user',)

