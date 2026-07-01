from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import Conversation, Message

_ONLINE_THRESHOLD = timedelta(minutes=2)


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "conversation", "sender", "sender_username", "text", "is_read", "created_at"]
        read_only_fields = ["id", "sender", "sender_username", "is_read", "created_at"]


class ConversationSerializer(serializers.ModelSerializer):
    participant_ids = serializers.SerializerMethodField()
    participant_names = serializers.SerializerMethodField()
    participant_online = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id", "participant_ids", "participant_names", "participant_online",
            "last_message", "unread_count", "updated_at",
        ]

    def _participant_rows(self, obj):
        return list(obj.participants.order_by("id").values("id", "username", "last_seen"))

    def get_participant_ids(self, obj):
        return [r["id"] for r in self._participant_rows(obj)]

    def get_participant_names(self, obj):
        return [r["username"] for r in self._participant_rows(obj)]

    def get_participant_online(self, obj):
        cutoff = timezone.now() - _ONLINE_THRESHOLD
        return [
            r["last_seen"] is not None and r["last_seen"] >= cutoff
            for r in self._participant_rows(obj)
        ]

    def get_last_message(self, obj):
        msg = obj.messages.order_by("-created_at").first()
        if msg:
            return {"text": msg.text, "sender": msg.sender.username, "created_at": msg.created_at}
        return None

    def get_unread_count(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0
