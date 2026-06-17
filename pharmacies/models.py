from django.conf import settings
from django.db import models


class Pharmacy(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pharmacy",
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    phone = models.CharField(max_length=30)
    accent = models.CharField(max_length=10, blank=True)

    class Meta:
        db_table = "pharmacies"
        verbose_name_plural = "pharmacies"
        indexes = [
            models.Index(fields=["name"], name="idx_pharmacy_name"),
        ]

    def __str__(self):
        return self.name
