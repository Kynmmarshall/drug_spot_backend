from django.contrib import admin
from .models import DeviceToken, NotificationPreference


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "platform", "active", "updated_at"]
    list_filter = ["platform", "active"]


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ["user", "new_message", "request_update", "new_medicine"]
