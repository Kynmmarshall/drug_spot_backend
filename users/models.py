from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserType(models.TextChoices):
        PHARMACY = "pharmacy", "Pharmacy"
        PATIENT = "patient", "Patient"

    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    avatar_path = models.CharField(max_length=255, blank=True)
    user_type = models.CharField(max_length=20, choices=UserType.choices)
    last_seen = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
