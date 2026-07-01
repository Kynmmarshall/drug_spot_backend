from rest_framework import serializers
from .models import Medicine


class MedicineSerializer(serializers.ModelSerializer):
    pharmacy_id = serializers.IntegerField(source="pharmacy.id", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = ["id", "name", "price", "description", "pharmacy_id", "image_url"]

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class MedicineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["id", "name", "price", "description", "image"]
