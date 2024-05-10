from rest_framework import serializers
from .models import Post, Comment, Reports, Tag, Image
from Account.models import User
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import datetime, timedelta


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "pic"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "time_stamp", "author", "text", "post"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]

    def to_internal_value(self, data):
        # Overriding the default implementation
        # to check if a tag with the given name already exists.
        name = data.get("name")
        tag, created = Tag.objects.get_or_create(name=name)
        return tag


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ago = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"  # field for deserialization meaning field that will be used for create and update
        read_only_fields = [
            "author",
            "share_count",
            "vote_count",
            "ago",
            "comments",
        ]  #  field for serialization meaning field that will be retrieved

    def get_ago(self, obj):
        now = timezone.now()
        diff = now - obj.time_stamp

        if diff <= timedelta(minutes=60):
            return f"{diff.seconds // 60} minutes ago"
        elif diff <= timedelta(hours=24):
            return f"{diff.seconds // 3600} hours ago"
        elif diff <= timedelta(days=7):
            return f"{diff.days} days ago"
        else:
            return f"{diff.days // 7} weeks ago"

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        tags_data = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(post=post, **image_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data["name"])
            post.tags.add(tag_data)
        return post
        # for tag_data in tags_data:
        #     tag_serializer = TagSerializer(data=tag_data)
        #     if tag_serializer.is_valid():
        #         tag = tag_serializer.save()
        #         post.tags.add(tag)
        # return post

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images", [])
        tags_data = validated_data.pop("tags", [])
        instance.content = validated_data.get("content", instance.content)
        instance.post_type = validated_data.get("post_type", instance.post_type)
        instance.save()

        for image_data in images_data:
            Image.objects.update_or_create(post=instance, **image_data)

        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data["name"])
            instance.tags.add(tag)

        return instance
