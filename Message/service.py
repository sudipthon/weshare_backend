from channels.db import database_sync_to_async
from Message.models import Conversation, Messages
from Account.models import User
from django.db.models import Count

import logging

logger = logging.getLogger(__name__)
database_sync_to_async

database_sync_to_async
def get_user_instance(email=None, id=None):
    return User.objects.get(email=email) if email else User.objects.get(id=id)


database_sync_to_async
def get_user_details(email):
    user = User.objects.get(email=email)
    # domain = "http://127.0.0.1:8000"
    # img_url = f"{domain}{user.pic.url}"
    return {"username": user.username, "id": user.id, "pic": user.pic.url}


@database_sync_to_async
def create_message(conversation_id, message, user, receiver):
    receiver = get_user_instance(id=int(receiver))
    conversation = (
        Conversation.objects.filter(participants__in=[user, receiver])
        .annotate(num_participants=Count("participants"))
        .filter(num_participants=2)
        .first()
    )
    logger.info(conversation)
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(user, receiver)
        logger.info(conversation, "conersation created")
    message = Messages.objects.create(
        conversation=conversation, author=get_user_instance(user.email), text=message
    )
    message.save()


@database_sync_to_async
def get_messages(conversation_id, limit=10, offset=0):
    conversation = Conversation.objects.get(id=conversation_id)
    messages = Messages.objects.filter(conversation=conversation).order_by(
        "-time_stamp"
    )[offset:limit]
    message_searialized = [
        {
            "author": get_user_details(message.author.email),
            "text": message.text,
            "created_at": message.time_stamp.isoformat(),
        }
        for message in messages
    ]
    return message_searialized


@database_sync_to_async
def get_conversations(user):
    conversation_objs=user.conversations.all()
    conv_serialized = [
        {
            "id": conversation.id,
            "receiver": [
                get_user_details(u.email)
                for u in conversation.participants.all()
                if u != user
            ],
            "updated_at": conversation.updated_at.isoformat(),
            "last_message": conversation.last_message,
        }
        for conversation in conversation_objs
    ]
    return conv_serialized
