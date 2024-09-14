from django.db import models



class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    # Add any additional fields if needed

