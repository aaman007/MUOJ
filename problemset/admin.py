from django.contrib import admin

from problemset.models import Language, Problem, TestCase, Submission


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    pass


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    pass


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass
