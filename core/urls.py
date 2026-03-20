from django.urls import path
from core.views.auth_views import register, LoginView
from core.views.quiz_views import create_quiz, list_quizzes, quiz_detail, create_question, create_option
from core.views.attempt_views import start_attempt, submit_attempt, attempt_history, submit_answer
from core.views.analytics_views import quiz_analytics, user_analytics
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/login/", LoginView.as_view()),
    path("auth/register/", register),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("quizzes/", list_quizzes),
    path("quizzes/create/", create_quiz),
    path("questions/create/", create_question),
    path("option/create/", create_option),
    path("quizzes/<int:pk>/", quiz_detail), 
    path('attempts/', start_attempt),
    path('attempts/<int:pk>/submit/', submit_attempt),
    path('history/', attempt_history), 
    path('attempts/<int:pk>/answer/', submit_answer),
    path('analytics/', user_analytics),
    path('analytics/quiz/<int:quiz_id>/', quiz_analytics), 
]