from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User


class UserSerializer(serializers.ModelSerializer):
    # change_password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "is_active",
            #   "change_password"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    # def get_change_password(self, obj):
    #     return "http://127.0.0.1:8000/api/users/{}/change-password/".format(obj.id)
