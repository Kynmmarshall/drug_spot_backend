from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Pharmacy
from .serializers import PharmacySerializer


@api_view(["GET"])
def pharmacy_list(request):
    pharmacies = Pharmacy.objects.all()
    serializer = PharmacySerializer(pharmacies, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def pharmacy_detail(request, pk):
    try:
        pharmacy = Pharmacy.objects.get(pk=pk)
    except Pharmacy.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PharmacySerializer(pharmacy)
    return Response(serializer.data)
