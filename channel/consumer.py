import json

from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from channel.models import Channel, Message

User = get_user_model()


class MessageConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.channel = None
        self.group_name = None

    async def connect(self):
        self.channel = await self.get_channel()
        self.group_name = f"group_{self.channel.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        message = text_data.get('message')
        user = self.scope.get('user')

        if message and user.is_authenticated:
            await self.create_message(user=user, message=message)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "channel.message",
                    "text": json.dumps({
                        'message': message,
                        'username': user.username
                    }),
                }
            )

    async def channel_message(self, event):
        await self.send(event["text"])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    def get_channel(self, channel_slug=''):
        kwargs = self.scope.get('url_route', {}).get('kwargs', {})
        return Channel.objects.get(id=kwargs.get('pk'))

    @database_sync_to_async
    def create_message(self, user, message):
        return Message.objects.create(channel=self.channel, user=user, text=message)

