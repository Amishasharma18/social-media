
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    twitter_access_token = models.CharField(max_length=255, blank=True, null=True)
    twitter_access_token_secret = models.CharField(max_length=255, blank=True, null=True)  # ✅ ADD THIS

    facebook_access_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
