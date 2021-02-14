from django.contrib import admin

from core.models import Constant


@admin.register(Constant)
class ConstantAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'remote']
