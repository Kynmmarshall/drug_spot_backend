from django.urls import path
from . import views

urlpatterns = [
    path("", views.pharmacy_list),
    path("<int:pk>", views.pharmacy_detail),
]
