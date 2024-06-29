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


    
    

class User(AbstractUser):
    username=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    email=models.EmailField(max_length=100,unique=True)
    # bio=models.TextField(default='no bio...',max_length=300)
    pic=models.ImageField(default="images/goku.png",null=True,blank=True)
    
    USERNAME_FIELD='email' #this is the field that will be used to login instead of username
    REQUIRED_FIELDS=['username'] #this is the field that will be required to create a user
 
 
    def __str__(self):
        return f"{self.email} -{self.id}"