from django.conf import settings
from django.db import models


class DeviceToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="device_tokens",
    )
    token = models.TextField(unique=True)
    platform = models.CharField(max_length=10, choices=[("android", "Android"), ("ios", "iOS")])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_tokens"

    def __str__(self):
        return f"{self.user.username} ({self.platform})"


class NotificationPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_prefs",
    )
    new_message = models.BooleanField(default=True)
    request_update = models.BooleanField(default=True)
    new_medicine = models.BooleanField(default=True)

    class Meta:
        db_table = "notification_preferences"

    def __str__(self):
        return f"Prefs({self.user.username})"
