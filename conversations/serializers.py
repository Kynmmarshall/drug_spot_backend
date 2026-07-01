from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "conversation", "sender", "sender_username", "text", "is_read", "created_at"]
        read_only_fields = ["id", "sender", "sender_username", "is_read", "created_at"]


class ConversationSerializer(serializers.ModelSerializer):
    participant_ids = serializers.SerializerMethodField()
    participant_names = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "participant_ids", "participant_names", "last_message", "unread_count", "updated_at"]

    def get_participant_ids(self, obj):
        return list(obj.participants.values_list("id", flat=True))

    def get_participant_names(self, obj):
        return list(obj.participants.values_list("username", flat=True))

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
