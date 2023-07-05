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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1

class AuthSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=12,min_length=12)

class OtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6,min_length=6)
    phone = serializers.CharField(max_length=12,min_length=12)