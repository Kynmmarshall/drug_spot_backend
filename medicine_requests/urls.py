from django.urls import path
from . import views

urlpatterns = [
    path("", views.medicine_request_list),
]
