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
        user_group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(user_group_name, self.channel_name)

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

    # Add this method to handle the update signal
    async def update_conversations(self, event):
        await self.fetch_and_send_conversations()

    async def disconnect(self, code):
        return await super().disconnect(code)


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # await self.fetch_messages(10, 0)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message_type = data.get("type")
        if message_type == "new_message":
            message = data["message"]
            receiver = data["receiver"]
            time_stamp = data["time_stamp"]
            await create_message(
                self.conversation_id, message, self.scope["user"], receiver, time_stamp
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "new_message",
                    "message": message,
                    "time_stamp": time_stamp,
                },
            )

            # After saving the message successfully
            await self.channel_layer.group_send(
                f"user_{self.scope['user'].id}",
                {
                    "type": "update_conversations",
                },
            )
            await self.channel_layer.group_send(
                f"user_{receiver}",
                {
                    "type": "update_conversations",
                },
            )

        elif message_type == "fetch_messages":
            limit = data.get("limit", 10)
            offset = data.get("offset", 0)
            await self.fetch_messages(limit, offset)

    async def fetch_messages(self, limit, offset):
        messages = await get_messages(self.conversation_id, limit, offset)
        await self.send(
            text_data=json.dumps({"type": "previous_messages", "messages": messages})
        )

    async def new_message(self, event):
        message = event["message"]
        time_stamp = event["time_stamp"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "new_message",
                    "message": [
                        {
                            "text": message,
                            "created_at": time_stamp,
                        }
                    ],
                   
                }
            )
        )
        # await self.send(
        #     text_data=json.dumps(
        #         {
        #             "type": "new_message",
        #             "message": message,
        #             "created_at": time_stamp,
        #         }
        #     )
        # )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


# {
#   "type": "previous_messages",
#   "messages": [
#     {
#       "author": {
#         "username": "SHushma Khattri",
#         "id": 7,
#         "pic": "/media/shushma_profile.jpg"
#       },
#       "text": "hi",
#       "created_at": "2024-07-10T05:08:05.183922+00:00"
#     },


# https://bug12.pythonanywhere.com/
# ws://bug12.pythonanywhere.com/ws/conversations/?token=649ea14d67d3d3e03beccaf8b4fbb20759562d8
# ws://bug12.pythonanywhere.com/ws/chat/1/?token=649ea14d67d3d3e03beccaf8b4fbb20759562d87

# ws://localhost:8000/ws/conversations/?token=649ea14d67d3d3e03beccaf8b4fbb20759562d87
# ws://localhost:8000/ws/chat/1/?token=649ea14d67d3d3e03beccaf8b4fbb20759562d87
