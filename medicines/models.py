from django.db import models


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to="medicines/", blank=True)
    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name="medicines",
    )

    class Meta:
        db_table = "medicine_requests"

    def __str__(self):
        return f"{self.username} — {self.medicine_name}"