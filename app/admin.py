from django.contrib import admin
from app.models import Profile,Otp,CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Otp)
