from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from app.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields =["email","username"]

class SignupSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone']