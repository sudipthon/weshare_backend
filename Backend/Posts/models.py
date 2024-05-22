from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission


from Account.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    OPTIONS = (
        ("Scam", "Scam"),
        ("Sale & Buy", "Sale & Buy"),
    )
    post_type = (
       ( "Giveaway","Giveaway"),
        ("Exchange","Exchange"),
    )
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to="images/posts", default="default.jpg")
    share_count = models.PositiveIntegerField(default=0, blank=True)
    upvotes = models.ManyToManyField(User, related_name="votes", blank=True)
    tags = models.ManyToManyField(Tag, related_name="tag_posts", blank=True)
    flag = models.CharField(max_length=30, choices=OPTIONS, blank=True, null=True)
    post_type = models.CharField(max_length=30, choices=post_type)
    
    class Meta:
        ordering = ["-time_stamp"]

    def __str__(self):
        return f"{self.content[:50]}--{self.id}"
    

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/posts/", default="default.jpg")

class Comment(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=100, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.author.email


class Reports(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_reports"
    )
    reason = models.TextField(max_length=100, null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_reports"
    )
    


