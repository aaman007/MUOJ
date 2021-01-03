from django.contrib import admin

from problemset.models import Language, Problem, TestCase, Submission, Clarification


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'created_at']


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    pass


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['problem', 'contest', 'user', 'status', 'created_at']


@admin.register(Clarification)
class ClarificationAdmin(admin.ModelAdmin):
    pass
