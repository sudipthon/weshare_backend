import os
import django
from dotenv import load_dotenv

load_dotenv()

DJANGO_ENV = os.environ.get("DJANGO_ENV")

if DJANGO_ENV == "server":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeShare.server_settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeShare.local_settings")
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeShare.local_settings')
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
from django.conf import settings

from Message import consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeShare.settings")
django.setup()
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            TokenAuthMiddleware(
                AllowedHostsOriginValidator(
                    URLRouter(
                        # websocket_urlpatterns
                        [
                            re_path(
                                r"ws/chat/(?P<conversation_id>\d+)/$",
                                consumers.ChatConsumer.as_asgi(),
                            ),
                            re_path(
                                r"ws/conversations/$",
                                consumers.ConversationConsumer.as_asgi(),
                            ),
                        ]
                    )
                )
            )
        ),
        # Just HTTP for now. (We can add other protocols later.)
    }
)
