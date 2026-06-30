from django.db import models
from pharmacies.models import Pharmacy


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name="medicines",
    )

    class Meta:
        db_table = "medicines"
        indexes = [
            models.Index(fields=["name"], name="idx_medicine_name"),
        ]

    def __str__(self):
        return f"{self.name} - {self.pharmacy.name}"
