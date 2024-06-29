from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer, ConversationSerializer
from rest_framework.response import Response
from django.db.models import Q
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.db.models import Count

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

    def get_queryset(self):
        try:
            conversation = Conversation.objects.get(
                id=self.kwargs["conversation_pk"])
        except Conversation.DoesNotExist:
            raise Http404("Conversation not found.")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(
                "You do not have permission to access this conversation."
            )

        if not self.kwargs["conversation_pk"].isdigit():
            raise ValidationError("Conversation ID must be a number.")

        return Messages.objects.filter(conversation__id=self.kwargs["conversation_pk"])

    def create(self, request, *args, **kwargs):
        receiver_id = request.data.get("receiver")
        receiver = User.objects.get(id=receiver_id)
        if not receiver:
            return Response(
                {"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        conversation = (
            Conversation.objects.filter(
                participants__in=[request.user, receiver])
            .annotate(num_participants=Count("participants"))
            .filter(num_participants=2)
            .distinct()
        )
        if not conversation.exists():
            # If no such conversation exists, create a new one
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, receiver)
        else:
            # If a conversation does exist, get the first one
            conversation = conversation.first()

        request.data["conversation"] = conversation.id
        return super().create(request, *args, **kwargs)
