from .models import Room
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .serializers import RoomSerializer
from django.forms import model_to_dict


class RoomsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = Room.objects.all()
        room_data = RoomSerializer(rooms, many=True)
        return JsonResponse({"rooms": room_data.data})


class RoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        rooms = Room.objects.filter(label=slug)
        room_data = RoomSerializer(rooms, many=True)
        return JsonResponse({"rooms": room_data.data})


class CreateRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("room_name")
        print(name)
        room = Room(name=name)
        room.save()
        return JsonResponse({"room": model_to_dict(room)})
