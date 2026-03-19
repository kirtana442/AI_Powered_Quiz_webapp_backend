from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .auth_serializers import CustomTokenObtainPairSerializer

from drf_spectacular.utils import extend_schema

from .models import Quiz
from .serializers import QuizSerializer,RegisterSerializer

def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
        return JsonResponse({"stautus":"OK","db":"up"})
    except Exception as e:
        return JsonResponse(
            {"status":"error","db":"down","details":str(e)},
            status=500
        )
    
@extend_schema(
        request=QuizSerializer,
        responses=QuizSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_quiz(request):
    serializer = QuizSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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