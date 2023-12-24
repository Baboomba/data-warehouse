from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Info

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        exclude = ['password']


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Info
        fields = ['email', 'password', 'password2']


class TokenSerializer(serializers.ModelSerializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    
    class Meta:
        model = Info
        fields = ['email', 'password', 'access', 'refresh']