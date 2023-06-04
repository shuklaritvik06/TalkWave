from django.urls import path

from chat.consumers import ChatConsumer

websocket_urls = [
    path("ws/<str:room_name>/", ChatConsumer.as_asgi()),
]
