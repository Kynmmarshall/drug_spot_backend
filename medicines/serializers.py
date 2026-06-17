from rest_framework import serializers
from .models import Medicine


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["id", "name", "price", "pharmacy_id"]

    pharmacy_id = serializers.IntegerField(source="pharmacy.id", read_only=True)


class MedicineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["id", "name", "price"]
