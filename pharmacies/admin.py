from django.contrib import admin
from .models import Pharmacy


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "address", "phone"]
    search_fields = ["name", "address"]
