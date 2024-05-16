from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractUser


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         # Assign the default group to the user
#         # default_group = Group.objects.get(
#         #     name="normal_user"
#         # )  # replace 'default' with your default group name
#         # default_group.user_set.add(user)
#         # for app_config in apps.get_app_configs():
#         #     for model in app_config.get_models():
#         #         permissions = Permission.objects.filter(
#         #             content_type__app_label=app_config.label,
#         #             content_type__model=model._meta.model_name,
#         #         )
#         #         for permission in permissions:
#         #             user.user_permissions.add(permission)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self.create_user(email, password, **extra_fields)


# class User(AbstractBaseUser,PermissionsMixin):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100, unique=True)
#     is_verified = models.BooleanField(default=False)
#     pic = models.ImageField(upload_to="images/profile_pics",null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     # is_superuser = models.BooleanField(default=False)

#     groups = models.ManyToManyField(Group, related_name="custom_user_groups")
#     user_permissions = models.ManyToManyField(
#         Permission, related_name="custom_user_permissions"
#     )

#     objects = CustomUserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return f"{self.email} -{self.id}"

    
    

class User(AbstractUser):
    username=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    email=models.EmailField(max_length=100,unique=True)
    # bio=models.TextField(default='no bio...',max_length=300)
    pic=models.ImageField(default="goku.jpg",null=True,blank=True)
    
    USERNAME_FIELD='email' #this is the field that will be used to login instead of username
    REQUIRED_FIELDS=['username'] #this is the field that will be required to create a user
 
 
    def __str__(self):
        return f"{self.email} -{self.id}"