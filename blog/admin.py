from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from blog.models import Blog, Comment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'preference']
    list_filter = ['preference']
    actions = ['mark_preferred', 'unmark_preferred']

    def mark_preferred(self, request, queryset: Blog):
        queryset.update(preference=True)

    def unmark_preferred(self, request, queryset: Blog):
        queryset.update(preference=False)

    mark_preferred.short_description = _('Mark selected blogs as preferred')
    unmark_preferred.short_description = _('Unmark selected blogs as preferred')


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ['author', 'post_connected', 'comment']
