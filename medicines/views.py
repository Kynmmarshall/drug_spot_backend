from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Medicine
from .serializers import MedicineSerializer, MedicineCreateSerializer
from .permissions import IsPharmacyOwner


@api_view(["GET", "POST"])
def medicine_list(request):
    if request.method == "GET":
        medicines = Medicine.objects.all()
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data)

    if not request.user.is_authenticated or request.user.user_type != "pharmacy":
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    pharmacy = getattr(request.user, "pharmacy", None)
    if not pharmacy:
        return Response({"error": "Pharmacy not found"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = MedicineCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    medicine = serializer.save(pharmacy=pharmacy)
    return Response(MedicineSerializer(medicine).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def medicine_detail(request, pk):
    try:
        medicine = Medicine.objects.select_related("pharmacy").get(pk=pk)
    except Medicine.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data)

    if not request.user.is_authenticated or request.user.user_type != "pharmacy":
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    if medicine.pharmacy.user_id != request.user.id:
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "PUT":
        serializer = MedicineCreateSerializer(medicine, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True})

    medicine.delete()
    return Response({"success": True})


@api_view(["GET"])
def medicines_by_pharmacy(request, pk):
    medicines = Medicine.objects.filter(pharmacy_id=pk)
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)
