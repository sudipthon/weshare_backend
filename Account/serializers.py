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
            'email',
            #   "change_password"
            "password",
        ]
        read_only_fields = ["num_posts"]
        extra_kwargs = {"password": {"write_only": True}}
    
    def validate(self, data):
        # Custom validation logic here
        if not self.partial:
            # Perform certain validations only if it's not a partial update
            if not data.get('username'):
                raise serializers.ValidationError({"username": "This field may not be blank."})
            if not data.get('password'):
                raise serializers.ValidationError({"password": "This field may not be blank."})
        return data

    def get_num_posts(self, obj):
        return Post.objects.filter(author=obj).count()

    def create(self, validated_data):
        password = validated_data.pop("password")
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

    # def update(self, instance, validated_data):
    #     password = validated_data.pop("password", None)
    #     pic = validated_data.pop("pic", None)  
    #     username = validated_data.get('username', instance.username)

    #   # Update username and other fields
    #     instance.username = username
    #     if password is not None:
    #         instance.set_password(password)
    #     if pic is not None:
    #         instance.pic = pic  # Update the pic field if a new pic is provided
    #     instance.save()
    #     return instance
    # # def get_change_password(self, obj):
    # #     return "http://127.0.0.1:8000/api/users/{}/change-password/".format(obj.id)

    def update(self, instance, validated_data):
        update_fields = []

        # Check and update password
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)
            update_fields.append('password')

        # Check and update pic
        pic = validated_data.pop("pic", None)
        if pic is not None:
            instance.pic = pic
            update_fields.append('pic')

        # Check and update username
        username = validated_data.get('username', instance.username)
        if username != instance.username:
            instance.username = username
            update_fields.append('username')

        # Save instance with specified update fields if any field was updated
        if update_fields:
            instance.save(update_fields=update_fields)
        else:
            instance.save()

        return instance