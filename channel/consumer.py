import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from channel.models import Channel

User = get_user_model()


class MessageConsumer(AsyncConsumer):
    def __init__(self):
        super().__init__()
        self.channel = None
        self.group_name = None

    async def websocket_connect(self, event):
        self.channel = await self.get_channel()
        self.group_name = f"group_{self.channel.id}"
        self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        text = json.loads(event.get('text', '{}'))
        message = text.get('message')
        user = self.scope.get('user')
        if message:
            # broadcasts message event
            await self.channel_layer.group_send(self.group_name, {
                "type": "channel.message",
                "text": json.dumps({
                    "username": user.username,
                    "message": message
                })
            })

    async def channel_message(self, event):
        print(event)
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_channel(self, channel_slug=''):
        return Channel.objects.get(id=1)
