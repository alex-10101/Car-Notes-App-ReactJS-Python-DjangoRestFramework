from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    """ 
    Class which represents a custom user model 
    and which should be used instead if Django's default User model.
    Extends the AbstractUser class with the given attributes.
    """    
    email = models.EmailField(unique=True, blank=False, null=False, error_messages={
        "unique": "A user with this email already exists."
    })
