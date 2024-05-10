from django.db import models
from Account.models import User


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')

class Message(models.Model):
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,related_name='messages')
    image=models.ImageField(upload_to='images/messages', default='default.jpg')

    def __str__(self):
        return self.content
    