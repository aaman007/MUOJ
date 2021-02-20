from django.urls import path

from channel.views import ChannelListView, MessageListView, MessageCreateView

app_name = 'channel'

urlpatterns = [
    path('', ChannelListView.as_view(), name='channel-list'),
    path('<int:pk>/', MessageListView.as_view(), name='message-list'),
    path('<int:pk>/new/', MessageCreateView.as_view(), name='message-create')
]
