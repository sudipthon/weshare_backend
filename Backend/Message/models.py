from django.db import models
from Account.models import User




from django.db import models


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation between {', '.join([user.username for user in self.participants.all()])}  {self.id}"

    class Meta:
        ordering = [
            "-updated_at",
        ]


class Messages(models.Model):
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.SET_NULL, null=True
    )
    text = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="message_images/", blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = [
            "time_stamp",
        ]
