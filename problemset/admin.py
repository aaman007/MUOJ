from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from problemset.models import Language, Problem, TestCase, Submission, Clarification


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_filter = ['is_protected', 'memory_limit', 'time_limit']
    list_display = ['name', 'author', 'created_at', 'is_protected', 'memory_limit', 'time_limit']
    fieldsets = (
        (_('General'), {
            'fields': ['name', 'statement', 'input_section', 'output_section', 'editorial']
        }),
        (_('Configuration'), {
            'fields': ['is_protected', 'time_limit', 'memory_limit']
        }),
        (_('Others'), {
            'fields': ['solution_language', 'solution', 'author']
        })
    )


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['problem', 'is_sample', 'label']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['problem', 'contest', 'user', 'status', 'created_at', 'modified_at']
    list_filter = ['status']


@admin.register(Clarification)
class ClarificationAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'user', 'contest', 'problem']
