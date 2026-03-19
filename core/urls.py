from django.urls import path
from .views import health, create_quiz, register, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("quizzes/",create_quiz),
    path("health/",health),
    path("auth/login/", LoginView.as_view()),
    path("auth/register/", register),
    path("auth/refresh/", TokenRefreshView.as_view()),   
]