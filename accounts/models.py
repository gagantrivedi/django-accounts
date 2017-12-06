from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    email_id = models.EmailField(unique=True)
    profile_picture_url = models.URLField()
