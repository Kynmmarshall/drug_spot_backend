from django.urls import path
from . import views

urlpatterns = [
    path("", views.conversation_list),
    path("start", views.start_conversation),
    path("<int:conversation_id>/messages", views.message_list),
    path("<int:conversation_id>/send", views.send_message),
]
