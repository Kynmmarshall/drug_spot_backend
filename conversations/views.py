from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def conversation_list(request):
    conversations = request.user.conversations.all()
    serializer = ConversationSerializer(
        conversations, many=True, context={"request": request}
    )
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_conversation(request):
    other_user_id = request.data.get("user_id")
    if not other_user_id:
        return Response({"error": "user_id required"}, status=status.HTTP_400_BAD_REQUEST)

    if int(other_user_id) == request.user.id:
        return Response({"error": "Cannot message yourself"}, status=status.HTTP_400_BAD_REQUEST)

    existing = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user_id
    ).first()

    if existing:
        serializer = ConversationSerializer(existing, context={"request": request})
        return Response(serializer.data)

    conversation = Conversation.objects.create()
    conversation.participants.add(request.user.id, other_user_id)
    serializer = ConversationSerializer(conversation, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def message_list(request, conversation_id):
    try:
        conversation = Conversation.objects.get(
            id=conversation_id, participants=request.user
        )
    except Conversation.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    conversation.messages.filter(is_read=False).exclude(
        sender=request.user
    ).update(is_read=True)

    messages = conversation.messages.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request, conversation_id):
    try:
        conversation = Conversation.objects.get(
            id=conversation_id, participants=request.user
        )
    except Conversation.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    text = request.data.get("text", "").strip()
    if not text:
        return Response({"error": "text required"}, status=status.HTTP_400_BAD_REQUEST)

    message = Message.objects.create(
        conversation=conversation, sender=request.user, text=text
    )
    conversation.save()

    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
