from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from accounts.models import Profile

User = get_user_model()

admin.site.site_header = "MUOJ Admin Panel"
admin.site.site_title = "MU Online Judge"
admin.site.index_title = "MU Online Judge Admin Panel"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
    fieldsets = [
        [None, {'fields': ['username', 'password']}],
        [_('Personal info'), {'fields': ['first_name', 'last_name', 'email']}],
        [_('Permissions'), {
            'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'],
        }],
        [_('Important dates'), {'fields': ['last_login', 'date_joined']}]
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'rank', 'levels_completed']
    list_filter = ['rank']

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass
