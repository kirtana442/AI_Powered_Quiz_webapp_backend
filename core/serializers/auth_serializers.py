from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","password"]
        extra_kwargs = {
            "password": {"write_only":True}
        }

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): 
    def validate(self,attrs): 
        data = super().validate(attrs) 
        data["user"] = { 
            "id": self.user.id,
            "username": self.user.username,
            "role": self.user.profile.role,
        }
        return data