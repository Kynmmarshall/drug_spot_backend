from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DeviceToken, NotificationPreference
from .serializers import DeviceTokenSerializer, NotificationPreferenceSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_device(request):
    token = request.data.get("token")
    platform = request.data.get("platform", "android")

    if not token:
        return Response({"error": "token required"}, status=status.HTTP_400_BAD_REQUEST)

    device, created = DeviceToken.objects.update_or_create(
        token=token,
        defaults={"user": request.user, "platform": platform, "active": True},
    )
    return Response(DeviceTokenSerializer(device).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unregister_device(request):
    token = request.data.get("token")
    if token:
        DeviceToken.objects.filter(token=token, user=request.user).update(active=False)
    return Response({"success": True})


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def notification_preferences(request):
    prefs, _ = NotificationPreference.objects.get_or_create(user=request.user)

    if request.method == "GET":
        return Response(NotificationPreferenceSerializer(prefs).data)

    serializer = NotificationPreferenceSerializer(prefs, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
