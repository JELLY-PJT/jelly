# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<int:group_pk>/", consumers.ChatConsumer.as_asgi()),
]