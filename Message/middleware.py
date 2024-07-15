import logging
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs


logger = logging.getLogger(__name__)


@database_sync_to_async
def get_user_from_token(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return None

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

        
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope['query_string'].decode())
        token_key = query_string.get('token', [None])[0]
        user=None
    
        if token_key:
            user = await get_user_from_token(token_key)
            if user is None:
                logger.warning("Invalid token provided. Connection closed.")
                await send({
                    'type': 'websocket.close',
                    'code': 4001
                })
                return
        else:
            logger.warning("No token provided. Connection closed.")
            await send({
                'type': 'websocket.close',
                'code': 4000
            })
            return

        scope['user'] = user if user else AnonymousUser()
        return await self.inner(scope, receive, send)
