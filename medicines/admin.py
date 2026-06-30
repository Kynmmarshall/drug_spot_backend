from django.contrib import admin
from .models import User

admin.site.register(User)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "pharmacy"]
    list_filter = ["pharmacy"]
    search_fields = ["name"]
