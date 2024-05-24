from django.db import models
from Account.models import User


# class Conversation(models.Model):
#     # user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_user1')
#     # user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_user2')

#     name=models.CharField(max_length=100)

#     def save(self):
#         self.name=self.messages__receiver


# class Messages(models.Model):
#     content = models.TextField()
#     time_stamp = models.DateTimeField(auto_now_add=True)
#     sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender')
#     receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='receiver')
#     image=models.ImageField(upload_to='images/messages', default='default.jpg', blank=True, null=True)
#     conversation=models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
#     def __str__(self):
#         return self.content
#     class Meta:
#         ordering = ['time_stamp',]


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
        # receiver=self.conversation.participants.exclude(id=self.author.id).first()
        # return f"{self.conversation.id}:{self.author}-{receiver}----{self.id}"
        return self.text

    class Meta:
        ordering = [
            "time_stamp",
        ]
