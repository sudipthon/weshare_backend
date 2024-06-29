# serializers.py
from rest_framework import serializers
from .models import Conversation, Messages
from Account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "pic", "id"]


class MessageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Messages
        fields = ["conversation", "author", "text", "time_stamp", "image"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    messages = MessageSerializer(
        many=True, read_only=True, source="messages_set")

    class Meta:
        model = Conversation
        fields = ["participants", "updated_at", "messages"]

    def get_participants(self, obj):
        # Filter out the current user
        participants = [
            user
            for user in obj.participants.all()
            if user != self.context["request"].user
        ]
        # Serialize the remaining users
        return UserSerializer(participants, many=True).data
