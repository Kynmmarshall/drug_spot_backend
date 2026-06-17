from rest_framework import serializers
from .models import MedicineRequest


class MedicineRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineRequest
        fields = ["id", "username", "contact", "medicine_name", "avatar_path", "use_asset"]
