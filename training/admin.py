from django.contrib import admin

from training.models import Tutorial


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    pass
