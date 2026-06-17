from django.urls import path
from . import views

urlpatterns = [
    path("", views.medicine_list),
    path("<int:pk>", views.medicine_detail),
    path("pharmacy/<int:pk>", views.medicines_by_pharmacy),
]
