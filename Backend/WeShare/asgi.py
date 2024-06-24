"""
ASGI config for WeShare project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application
from Message.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator

from Message.middleware import TokenAuthMiddleware
from django.urls import re_path

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
from Message import consumers
django_asgi_app = get_asgi_application()
# django.setup()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":AuthMiddlewareStack(
        TokenAuthMiddleware(
        AllowedHostsOriginValidator(
        
        
        URLRouter(
            # websocket_urlpatterns
            [    re_path(r'ws/chat/(?P<conversation_id>\d+)/$', consumers.ChatConsumer.as_asgi()),]
        )
    ))
    )
    # Just HTTP for now. (We can add other protocols later.)
})