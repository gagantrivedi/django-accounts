from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    email_id = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    profile_picture_url = models.URLField()

    def __str__(self):
        return self.username + ' ' + self.email_id
