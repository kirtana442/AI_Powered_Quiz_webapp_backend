from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers.auth_serializers import CustomTokenObtainPairSerializer, RegisterSerializer

@extend_schema(
        request=RegisterSerializer,
        responses=RegisterSerializer,
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response({
            "message": "User created successfully",
            "username": user.username
        }, status = status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=400)

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]