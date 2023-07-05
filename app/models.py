from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=12,null=False,blank=False,unique=True)
    profile_picture = models.ImageField(upload_to="profile_pictures",null=True,blank=True)
    proffession = models.JSONField(null=True,blank=True)
    interest = models.JSONField(null=True,blank=True)
    working_days = models.JSONField(null=True,blank=True)
    working_time_start = models.TimeField(null=True,blank=True)
    working_time_end = models.TimeField(null=True,blank=True)
    about = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.user.username


class Otp(models.Model):
    otp = models.CharField(max_length=6,null=False,blank=False)
    number = models.ForeignKey(Profile,on_delete=models.CASCADE)
    date_sent = models.DateTimeField(blank=False,null=False,default=timezone.now())

    def __str__(self) -> str:
        return self.number.phone