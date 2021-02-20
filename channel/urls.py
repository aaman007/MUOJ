from django.urls import path

from channel.views import MessageListView, MessageCreateView

app_name = 'channel'

urlpatterns = [
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create')
]
