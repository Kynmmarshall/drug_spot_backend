from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Pharmacy
from .serializers import PharmacySerializer, CreatePharmacySerializer


@api_view(["GET", "POST"])
def pharmacy_list(request):
    if request.method == "GET":
        pharmacies = Pharmacy.objects.all()
        serializer = PharmacySerializer(pharmacies, many=True)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.user_type != "pharmacy":
        return Response({"error": "Only pharmacy accounts can create pharmacies"}, status=status.HTTP_403_FORBIDDEN)

    if Pharmacy.objects.filter(user=request.user).exists():
        return Response({"error": "You already have a pharmacy registered"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CreatePharmacySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(PharmacySerializer(serializer.instance).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def pharmacy_detail(request, pk):
    try:
        pharmacy = Pharmacy.objects.get(pk=pk)
    except Pharmacy.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PharmacySerializer(pharmacy)
    return Response(serializer.data)
