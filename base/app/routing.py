from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/progress/', consumers.DownloadProgressConsumer.as_asgi()),
]
