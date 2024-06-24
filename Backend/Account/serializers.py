from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from Posts.models import Post


class UserSerializer(serializers.ModelSerializer):
    # change_password = serializers.SerializerMethodField()
    num_posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "pic",
            "num_posts",
            'email'
            #   "change_password"
        ]
        read_only_fields = ["num_posts"]
        extra_kwargs = {"password": {"write_only": True}}

    def get_num_posts(self, obj):
        return Post.objects.filter(author=obj).count()

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        email = validated_data.get("email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "A user with this email already exists."}
            )
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # def get_change_password(self, obj):
    #     return "http://127.0.0.1:8000/api/users/{}/change-password/".format(obj.id)
