from django.urls import path
from .views import RoomsView, RoomView, CreateRoomView

urlpatterns = [
    path("rooms/", RoomsView.as_view(), name="rooms"),
    path("room/<slug:slug>", RoomView.as_view(), name="room"),
    path("room/create/", CreateRoomView.as_view(), name="create_room"),
]
