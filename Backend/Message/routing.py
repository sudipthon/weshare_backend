from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conversation_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    # re_path(r'ws/conversations/$', consumers.ConversationConsumer.as_asgi()),


]
# r'ws/chat/(?P<conversation_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$'
