from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userinfo')

    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nickname
    

class PetInfo(models.Model):
    pet_name = models.CharField(max_length=30, null=True)
    pet_birth = models.DateField(verbose_name="반려동물 출생일", null=True)
    pet_anniv = models.DateField(verbose_name="반려동물 사망일", null=True)
    pet_image = models.ImageField(null=True, blank=True, upload_to='pet_images')
    pet_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='my_pets', null=True)

    TYPE_CHOICES = (
        ('강아지', '강아지'),
        ('고양이', '고양이'),
        ('소동물', '소동물'),
        ('기타', '기타')
    )
    pet_type = models.CharField(max_length=5, null=True, choices=TYPE_CHOICES)

    def __str__(self):
        return self.pet_name