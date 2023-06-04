from django.http import JsonResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hello(request):
    return JsonResponse({"message": "API is UP!", "status": "Logged In"})
