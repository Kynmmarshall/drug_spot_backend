from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/pharmacies/", include("pharmacies.urls")),
    path("api/medicines/", include("medicines.urls")),
    path("api/medicine_requests/", include("medicine_requests.urls")),
    path("api/conversations/", include("conversations.urls")),
    path("api/notifications/", include("notifications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
