from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from contest.models import Contest, Announcement


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author__username']
    list_display = ['title', 'start_time', 'duration', 'is_rated', 'rating_applied', 'author']
    list_filter = ['is_rated', 'rating_applied']

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'contest']


