from django.contrib import admin
from django.contrib.auth import get_user_model


class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'group',
        'level'
    ]

    raw_id_fields = ('group',)


# noinspection PyProtectedMember
class CohortUserInline(admin.TabularInline):
    model = None
    team_model = None

    @property
    def raw_id_fields(self):
        return [
            get_user_model()._meta.model_name,
            self.team_model._meta.model_name,
        ]


class CohortAdmin(admin.ModelAdmin):
    exclude = ('users',)
