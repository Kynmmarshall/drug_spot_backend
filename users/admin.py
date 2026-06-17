from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "user_type", "is_active"]
    list_filter = ["user_type", "is_active"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Drug Spot", {"fields": ("phone", "bio", "avatar_path", "user_type")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Drug Spot", {"fields": ("email", "phone", "user_type")}),
    )
