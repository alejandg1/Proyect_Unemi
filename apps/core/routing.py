from django.urls import re_path
from .consumers import DallEChat

websocket_urlpatterns = [
    re_path('dallechat', DallEChat.as_asgi()),
]
