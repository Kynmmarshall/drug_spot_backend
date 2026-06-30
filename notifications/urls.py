from django.urls import path
from . import views

urlpatterns = [
    path("device/register", views.register_device),
    path("device/unregister", views.unregister_device),
    path("preferences", views.notification_preferences),
]
