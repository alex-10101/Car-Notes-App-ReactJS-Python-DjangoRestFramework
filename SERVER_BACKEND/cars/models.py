from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Car(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    motor = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)




