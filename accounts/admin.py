from django.contrib import admin
from django.contrib.auth.models import Permission
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from accounts.models import Profile


admin.site.site_header = "MUOJ Admin Panel"
admin.site.site_title = "MU Online Judge"
admin.site.index_title = "MU Online Judge Admin Panel"


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
