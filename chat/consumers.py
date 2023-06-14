# chat/consumers.py
import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from groups.models import Group
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
import datetime


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["group_pk"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        user_pk = data["user_pk"]
        group_pk = data["group_pk"]
        nickname = data["nickname"]
        image = data["image"]

        user = await sync_to_async(User.objects.get)(pk=user_pk)
        group = await sync_to_async(Group.objects.get)(pk=group_pk)

        await self.save_message(user_pk, group_pk, message)

        messages = await sync_to_async(Message.objects.filter)(user=user, group=group)
        new_message = await sync_to_async(messages.last)()
        await sync_to_async(print)(new_message.created_at)
        message_time = new_message.created_at
        created_time = await sync_to_async(message_time.isoformat)()


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user_pk": user_pk,
                "group_pk": group_pk,
                "nickname": nickname,
                "image": image,
                "created_time": created_time,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user_pk = event["user_pk"]
        group_pk = event["group_pk"]
        nickname = event["nickname"]
        image = event["image"]
        created_time = event["created_time"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "user_pk": user_pk,
            "group_pk": group_pk,
            "nickname": nickname,
            "image": image,
            "created_time": created_time,
        }))
    
    @sync_to_async
    def save_message(self, user_pk, group_pk, message):
        user = User.objects.get(pk=user_pk)
        group = Group.objects.get(pk=group_pk)
        if message != '':
            return Message.objects.create(user=user, group=group, content=message)
