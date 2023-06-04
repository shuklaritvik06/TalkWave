from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import Message, Room
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "room_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.room_name)
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.join",
                "message": f"{self.scope['user'].username} joined the chat",
                "user": "admin",
                "room": f"{self.room_name}",
            },
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.room_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.leave",
                "message": f"{self.scope['user'].username} leaved the chat",
                "user": "admin",
                "room": f"{self.room_name}",
            },
        )

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        room = data["room"]
        await self.save_message(user=username, message=message, room=room)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
                "user": username,
                "room": room,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        room = event["room"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "user": username,
                    "room": room,
                }
            )
        )

    async def chat_leave(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "user": event["user"],
                    "room": event["room"],
                }
            )
        )

    async def chat_join(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "user": event["user"],
                    "room": event["room"],
                }
            )
        )

    @sync_to_async
    def save_message(self, user, room, message):
        user = User.objects.filter(username=user).get()
        room = Room.objects.filter(label=room).get()
        Message.objects.create(user=user, room=room, message=message)
