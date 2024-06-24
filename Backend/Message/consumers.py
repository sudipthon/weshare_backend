from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"
     
           # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)


        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data=json.loads(text_data)
        message=text_data['message']
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message}
        )
    
    async def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message+'hi'
        }))
      

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # Called when the socket closes