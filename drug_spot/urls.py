from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/pharmacies/", include("pharmacies.urls")),
    path("api/medicines/", include("medicines.urls")),
    path("api/medicine_requests/", include("medicine_requests.urls")),
]
