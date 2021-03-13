from django.contrib import admin

from channel.models import Channel, Message


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['text', 'channel', 'user']
    list_filter = ['channel']
