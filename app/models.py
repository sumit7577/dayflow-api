from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from app.manager import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
# Create your models here.


class CustomUser(AbstractUser):
    username_validator = ASCIIUsernameValidator
    username = models.CharField(_("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },)
    email = models.EmailField(_('email address'), unique=True,null=True,blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    phone = models.CharField(max_length=12,null=False,blank=False,unique=True,validators=[
        MinLengthValidator(12,"Please Enter 10 digit mobile phone number")
    ])
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