from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MedicineRequest
from .serializers import MedicineRequestSerializer


@api_view(["GET", "POST"])
def medicine_request_list(request):
    if request.method == "GET":
        requests_qs = MedicineRequest.objects.all()
        serializer = MedicineRequestSerializer(requests_qs, many=True)
        return Response(serializer.data)

    serializer = MedicineRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
