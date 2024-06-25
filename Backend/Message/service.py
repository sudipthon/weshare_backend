from channels.db import database_sync_to_async
from Message.models import Conversation, Messages
from Account.models import User

import logging

logger = logging.getLogger(__name__)

database_sync_to_async
def get_user_instance(email):
    return User.objects.get(email=email)

database_sync_to_async
def get_user_details(email):
    user=User.objects.get(email=user)
    return {"username": email.username, "id": user.id, "pic": user.pic.url}

@database_sync_to_async
def create_message(conversation_id, message,user):
    conversation=Conversation.objects.get(id=conversation_id)
    message = Messages.objects.create(conversation=conversation, author=get_user_instance(user.email), text=message)
    message.save()

@database_sync_to_async
def get_messages(conversation_id,limit=10,offset=0):
    conversation=Conversation.objects.get(id=conversation_id)
    messages=Messages.objects.filter(conversation=conversation).order_by("-time_stamp")[offset:limit]
    message_searialized=[{"author": get_user_details(message.author.email), "text": message.text, "created_at": message.time_stamp.isoformat()} for message in messages]
    return message_searialized
    

@database_sync_to_async
def get_conversations(user):
    # Fetch all conversations for the user
    conv=Conversation.objects.filter(participants=user)
    conv=[{"id": conversation.id, "participants": [get_user_details(u.email) for u in conversation.participants.all() if u!=user], "updated_at": conversation.updated_at.isoformat()} for conversation in conv]        
    return conv