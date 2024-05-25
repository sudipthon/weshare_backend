from rest_framework import serializers
from .models import Post, Comment, Reports, Tag, Image
from Account.models import User
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.datastructures import MultiValueDict


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "pic", "id"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image"]

    def to_internal_value(self, data):
        if isinstance(data, MultiValueDict):
            # Handle MultiValueDict
            print(data)
            images = data.getlist("[image]")
            if images:
                image = images[0]
            else:
                raise serializers.ValidationError("The image field is required.")
        else:
            # Handle regular dict
            image = data.get("image")
            if not image:
                raise serializers.ValidationError("The image field is required.")

        return image


class CommentSerializer(serializers.ModelSerializer):
    # parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)
    author = UserSerializer(read_only=True)
    time_stamp=serializers.SerializerMethodField()
    replies=serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ["id", "time_stamp", "author","time_stamp", "text", "replies"]
    
    def create(self, validated_data):
        parent = validated_data.pop('parent', None)
        comment = Comment.objects.create(**validated_data)
        if parent is not None:
            comment.parent = parent
            comment.save()
        return comment
    
    def get_time_stamp(self, obj):
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
        
    # def get_replies(self, obj):
    #     if obj.reply is not None:
    #         return CommentSerializer(obj.reply).data
    #     return None
    def get_replies(self, obj):
        replies = Comment.objects.filter(reply=obj)
        return CommentSerializer(replies, many=True).data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name",]

    def to_internal_value(self, data):
        if isinstance(data, MultiValueDict):
            # Handle MultiValueDict
            names = data.getlist("[name]")
            if names:
                name = names[0]
            else:
                raise serializers.ValidationError("The name field is required.")
        else:
            # Handle regular dict
            name = data.get("name")
            if not name:
                raise serializers.ValidationError("The name field is required.")

        tag, created = Tag.objects.get_or_create(name=name)
        return tag


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ago = serializers.SerializerMethodField()
    vote_count=serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'time_stamp',
            'author',
            'images',
            'tags',
            'post_type',
            'share_count',
            'vote_count',
            'ago',
            # 'comments',
            
        
            ]  # field for deserialization meaning field that will be used for create and update
        read_only_fields = [
            "author",
            "share_count",
            "vote_count",
            "ago",
            # "comments",
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
        
    def get_vote_count(self, instance):
        return instance.upvotes.count()

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])

        tags_data = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)
        for image_data in images_data:
            image_serializer = ImageSerializer(data={"image": image_data})
            if image_serializer.is_valid():
                Image.objects.create(post=post, image=image_serializer.validated_data)

        for tag_data in tags_data:
            post.tags.add(tag_data)

        return post

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
