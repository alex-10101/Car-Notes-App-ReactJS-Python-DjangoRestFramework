from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    """ 
    Class which represents a custom user model 
    and which should be used instead if Django's default User model.
    Extends the AbstractUser class with the given attributes.
    """    

    # Account will be inactive until email is verified.
    # If the account is inactive, the user cannot login.
    # is_active = models.BooleanField(default=False)  
