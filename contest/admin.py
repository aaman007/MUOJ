from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_json_widget.widgets import JSONEditorWidget

from contest.models import Contest, Announcement


class ContestStateFilter(admin.SimpleListFilter):
    title = _('State')
    parameter_name = 'state'

    def lookups(self, request, model_admin):
        return (
            (0, _('Running')),
            (1, _('Upcoming')),
            (2, _('Past Contests'))
        )

    def queryset(self, request, queryset: Contest):
        if self.value() == '0':
            return Contest.objects.running_contests()
        elif self.value() == '1':
            return Contest.objects.upcoming_contests()
        return Contest.objects.past_contests()


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author__username']
    list_display = ['title', 'start_time', 'duration', 'is_rated', 'rating_applied', 'author']
    list_filter = ['is_rated', 'rating_applied', ContestStateFilter]
    fieldsets = (
        (_('General'), {
            'fields': ['title', 'description', 'start_time', 'duration']
        }),
        (_('Configuration'), {
            'fields': ['openness', 'is_rated', 'rating_applied']
        }),
        (_('Problemset'), {
            'fields': ['problem_ids', 'problem_scores']
        }),
        (_('Others'), {
            'fields': ['author', 'contestants', 'standings']
        })
    )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'contest']


