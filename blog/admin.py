from django.contrib import admin
from .models import Blog, Comment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'preference']
    list_filter = ['preference']


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ['author', 'post_connected', 'comment']
