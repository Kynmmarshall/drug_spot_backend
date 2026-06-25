import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group = f"chat_{self.conversation_id}"

        user = self.scope.get("user")
        if not user or user.is_anonymous:
            await self.close()
            return

        is_participant = await self._is_participant(user.id)
        if not is_participant:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get("text", "").strip()
        if not text:
            return

        user = self.scope["user"]
        message = await self._save_message(user.id, text)

        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat_message",
                "id": message.id,
                "text": message.text,
                "sender": user.id,
                "sender_username": user.username,
                "created_at": message.created_at.isoformat(),
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "text": event["text"],
            "sender": event["sender"],
            "sender_username": event["sender_username"],
            "created_at": event["created_at"],
        }))

    @database_sync_to_async
    def _is_participant(self, user_id):
        return Conversation.objects.filter(
            id=self.conversation_id, participants__id=user_id
        ).exists()

    @database_sync_to_async
    def _save_message(self, user_id, text):
        conversation = Conversation.objects.get(id=self.conversation_id)
        message = Message.objects.create(
            conversation=conversation, sender_id=user_id, text=text
        )
        conversation.save()
        return message
