from django.db import models

class MedicineRequest(models.Model):
    username = models.CharField(max_length=150)
    contact = models.CharField(max_length=100)
    medicine_name = models.CharField(max_length=255)
    avatar_path = models.CharField(max_length=255, blank=True)
    use_asset = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "medicine_requests"

    def __str__(self):
        return f"{self.username} — {self.medicine_name}"