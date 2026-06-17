from django.contrib import admin
from .models import MedicineRequest


@admin.register(MedicineRequest)
class MedicineRequestAdmin(admin.ModelAdmin):
    list_display = ["username", "medicine_name", "contact"]
    search_fields = ["username", "medicine_name"]
