from django.contrib import admin

from contest.models import Contest, Announcement, Clarification


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    pass


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    pass


@admin.register(Clarification)
class ClarificationAdmin(admin.ModelAdmin):
    pass
