from django.db import models
from Account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


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

    def save(self, *args, **kwargs):
        if not self.id:  # If this is a new object, then set updated_at to now
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def last_message(self):
        return self.messages.latest("time_stamp").text if self.messages.exists() else None


class Messages(models.Model):
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.SET_NULL, null=True
    )
    text = models.TextField()
    time_stamp = models.DateTimeField()
    image = models.ImageField(upload_to="message_images/", blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = [
            "-time_stamp",
        ]



@receiver(post_save, sender=Messages)
def update_conversation_timestamp(sender, instance, created, **kwargs):
    if created:
        conversation = instance.conversation
        conversation.updated_at = (
            timezone.now()
        )  # Explicitly set updated_at to current time
        conversation.save()
