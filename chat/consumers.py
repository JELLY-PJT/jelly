# chat/consumers.py
import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from groups.models import Group
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    # async def fetch_messages(self, data):
    #     group_pk = int(self.group_pk)
    #     messages = Message.last_30_messages(self, group_pk=group_pk)
    #     content = {
    #         'command': 'messages',
    #         'messages': self.messages_to_json(messages)
    #     }
    #     self.send_message(content)

    # async def new_message(self, data):
    #     user_pk = data['user_pk']
    #     group_pk = data['group_pk']
    #     user_contact = User.objects.filter(user_id=user_pk)[0]
    #     group_contact = Group.objects.filter(group_id=group_pk)[0]
    #     message_create = Message.objects.create(
    #         user=user_contact,
    #         group=group_contact,
    #         message=data['message']
    #     )
    #     content = {
    #         'command': 'new_message',
    #         'message': self.message_to_json(message_create)
    #     }
    #     await self.send_chat_message(content)
    
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
        # created_at = data["created_at"]
        # user = User.objects.get(pk=user_pk)
        # group = Group.objects.get(pk=group_pk)

        await self.save_message(user_pk, group_pk, message)
        # created_at = await Message.get_latest_message(user, group)
        # if created_at:
        #     print(created_at)
        # else:
        #     print("메시지를 찾을 수 없습니다.")

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
                # "created_at": created_at,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user_pk = event["user_pk"]
        group_pk = event["group_pk"]
        nickname = event["nickname"]
        image = event["image"]
        # created_at = event["created_at"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "user_pk": user_pk,
            "group_pk": group_pk,
            "nickname": nickname,
            "image": image,
            # "created_at": created_at,
        }))
    
    @sync_to_async
    def save_message(self, user_pk, group_pk, message):
        user = User.objects.get(pk=user_pk)
        group = Group.objects.get(pk=group_pk)

        return Message.objects.create(user=user, group=group, content=message)
