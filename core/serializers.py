from rest_framework import serializers
from .models import Quiz
from django.contrib.auth.models import User

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
        read_only_fields = ["created_by"]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","password"]
        extra_kwargs = {
            "password": {"write_only":True}
        }

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)