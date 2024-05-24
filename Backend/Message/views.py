from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer, ConversationSerializer
from rest_framework.response import Response
from django.db.models import Q

# local imports
from .models import *


# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Messages
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return Messages.objects.filter(conversation__participants=self.request.user)

    def get_queryset(self):
        return Messages.objects.filter(conversation__id=self.kwargs["conversation_pk"])

    # def create(self, request, *args, **kwargs):
    #     receiver_username = request.data.get("receiver")
    #     receiver = User.objects.get(username=receiver_username)
    #     if not receiver:
    #         return Response(
    #             {"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    #     conversation, created = Conversation.objects.get_or_create(
    #         participants__in=[request.user, receiver], participants__count=2
    #     )

    #     request.data["conversation"] = conversation.id
    #     request.data["author"] = request.user.id
    #     return super().create(request, *args, **kwargs)
