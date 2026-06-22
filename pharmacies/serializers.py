from rest_framework import serializers
from .models import Pharmacy


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ["id", "user", "name", "address", "lat", "lng", "phone", "accent"]
        read_only_fields = ["user"]


class CreatePharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ["id", "name", "address", "lat", "lng", "phone", "accent"]
        read_only_fields = ["id"]
