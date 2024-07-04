from channels.generic.websocket import AsyncWebsocketConsumer
import json
from Message.middleware import get_user_from_token
from urllib.parse import parse_qs
from Message.service import *

import logging

logger = logging.getLogger(__name__)


class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = parse_qs(self.scope["query_string"].decode())
        token_key = query_string.get("token", [None])[0]
        user = await get_user_from_token(token_key)
        if user is None:
            logger.warning("Invalid token provided. Connection closed.")
            await self.close()
        self.user = user

        await self.accept()
        await self.fetch_and_send_conversations()

    async def receive(self, text_data=None):
        logger.info(text_data)
        data = json.loads(text_data)

        message_type = data.get("type")

        if message_type == "fetch_conversations":
            await self.fetch_and_send_conversations()

    async def fetch_and_send_conversations(self):
        conversations = await get_conversations(self.user)
        # Send the list of conversations to the client
        await self.send(
            text_data=json.dumps(
                {"type": "conversations_list", "conversations": conversations}
            )
        )

    async def disconnect(self, code):
        return await super().disconnect(code)


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.fetch_messages(20, 0)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message_type = data.get("type")
        receiver = data.get("receiver")
        if message_type == "chat_message":
            message = data["message"]
            await create_message(
                self.conversation_id, message, self.scope["user"], receiver
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                },
            )
        elif message_type == "fetch_messages":
            limit = data.get("limit", 20)
            offset = data.get("offset", 0)
            # messages = await get_messages(self.conversation_id, limit, offset)
            # await self.send(
            #     text_data=json.dumps(
            #         {"type": "previous_messages", "messages": messages}
            #     )
            # )
            # fetch_messages_task = self.fetch_messages(limit, offset)
            await self.fetch_messages(limit, offset)

    async def fetch_messages(self, limit, offset):
        messages = await get_messages(self.conversation_id, limit, offset)
        await self.send(
            text_data=json.dumps({"type": "previous_messages", "messages": messages})
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "author": self.scope["user"].username,
                }
            )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


# https://bug12.pythonanywhere.com/
# ws://bug12.pythonanywhere.com/ws/conversations/?token=649ea14d67d3d3e03beccaf8b4fbb20759562d8
# ws://bug12.pythonanywhere.com/ws/chat/1/?token=649ea14d67d3d3e03beccaf8b4fbb20759562d87

# ws://localhost:8000/ws/conversations/?token=649ea14d67d3d3e03beccaf8b4fbb20759562d87
# ws://localhost:8000/ws/chat/1/?token=649ea14d67d3d3e03beccaf8b4fbb20759562d87
