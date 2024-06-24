from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from Message.models import Conversation, Messages
from Message.middleware import get_user_from_token
from urllib.parse import parse_qs


@database_sync_to_async
def create_message(conversation_id, message,user):
    conversation=Conversation.objects.get(id=conversation_id)
    message = Messages.objects.create(conversation=conversation, author=user, text=message)
    message.save()

# @database_sync_to_async
# def get_conversation(conversation_id):
#     return Conversation.objects.get(id=conversation_id)

@database_sync_to_async
def get_messages(conversation_id,limit=10,offset=0):
    conversation=Conversation.objects.get(id=conversation_id)
    messages=Messages.objects.filter(conversation=conversation).order_by("-time_stamp")[offset:limit]
    return [{"author": message.author.username, "text": message.text, "created_at": message.time_stamp.isoformat()} for message in messages]
   
   
def get_conversations(user):
    # Fetch all conversations for the user
    return Conversation.objects.filter(conversations=user)

class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = parse_qs(self.scope['query_string'].decode())
        token_key = query_string.get('token', [None])[0]
        user=await get_user_from_token(token_key)
        if user is None:
            await self.close()
        self.user=user
        await self.accept()
        
    async def fetch_and_send_conversations(self):
        conversations = await get_conversations(self.user)
        serialized_conversations = [
            {
                'id': conversation.id,
                'title': conversation.title,
                'created_at': conversation.created_at.isoformat(),
                # Add more fields as needed
            }
            for conversation in conversations
        ]

        # Send the list of conversations to the client
        await self.send(text_data=json.dumps({
            'type': 'conversations_list',
            'conversations': serialized_conversations
        }))
        
    async def disconnect(self, code):
        return await super().disconnect(code)
    
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            message = data['message']
            await create_message(self.conversation_id, message, self.scope['user'])
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "message": message,
                    "author": self.scope['user'].username
                }
            )
        elif message_type == 'fetch_messages':
            limit = data.get('limit', 20)
            offset = data.get('offset', 0)
            messages = await get_messages(self.conversation_id, limit, offset)
            await self.send(text_data=json.dumps({
                'type': 'previous_messages',
                'messages': messages
            }))
    
    async def chat_message(self, event):
        message = event['message']
        await create_message(self.conversation_id, message, self.scope['user'])
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': self.scope['user'].username,
        }))
      

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # Called when the socket closes