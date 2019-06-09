from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chats/<room_name>', ChatConsumer),
]
