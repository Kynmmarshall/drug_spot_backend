"""
Utility for sending FCM push notifications.

Requires FIREBASE_CREDENTIALS_PATH in settings pointing to a
Firebase service account JSON file. Until that is configured,
send_push() is a no-op that logs the attempt.

Usage:
    from notifications.push import send_push_to_user
    send_push_to_user(user_id, title="New message", body="Hello!", data={"type": "chat"})
"""

import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)

_firebase_app = None


def _get_firebase():
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    creds_path = getattr(settings, "FIREBASE_CREDENTIALS_PATH", None)
    if not creds_path:
        logger.info("FIREBASE_CREDENTIALS_PATH not set — push notifications disabled")
        return None

    try:
        import firebase_admin
        from firebase_admin import credentials

        cred = credentials.Certificate(str(creds_path))
        _firebase_app = firebase_admin.initialize_app(cred)
        return _firebase_app
    except Exception as e:
        logger.warning("Failed to initialize Firebase: %s", e)
        return None


def send_push(token: str, title: str, body: str, data: dict | None = None):
    app = _get_firebase()
    if app is None:
        logger.info("Push skipped (no Firebase): %s → %s", title, token[:20])
        return False

    try:
        from firebase_admin import messaging

        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
            token=token,
        )
        messaging.send(message)
        return True
    except Exception as e:
        logger.warning("Push failed: %s", e)
        return False


def send_push_to_user(user_id: int, title: str, body: str, data: dict | None = None):
    from .models import DeviceToken

    tokens = DeviceToken.objects.filter(user_id=user_id, active=True).values_list("token", flat=True)
    for token in tokens:
        send_push(token, title, body, data)
