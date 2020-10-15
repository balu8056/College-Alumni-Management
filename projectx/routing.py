from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
#from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from alumni.consumers import ChatConsumer
from alumni import routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})