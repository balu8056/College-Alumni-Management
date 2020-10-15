from django.urls import path
from .consumers import ChatConsumer
from django.conf.urls import url

websocket_urlpatterns = [
    path('alumni/alumni', ChatConsumer),
]