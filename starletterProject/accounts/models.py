from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userinfo')

    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nickname