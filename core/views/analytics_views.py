from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.serializers.analytics_serializers import UserAnalyticsSerializer, QuizAnalyticsSerializer
from drf_spectacular.utils import extend_schema
from core.models import Attempt
from django.db.models import Avg, Max, Count, Q

@extend_schema(
        request=UserAnalyticsSerializer,
        responses=UserAnalyticsSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_analytics(request):
    if request.user.profile.role != 'ADMIN':
        return Response({"detail": "Only admins can view user analytics"}, status=403)

    attempts = Attempt.objects.all()

    data = {
        "total_attempts": attempts.count(),
        "completed_attempts": attempts.filter(status='COMPLETED').count(),
        "in_progress_attempts": attempts.filter(status='IN_PROGRESS').count(),
        "average_score": attempts.filter(status='COMPLETED').aggregate(
            avg=Avg('score')
        )['avg'] or 0,
        "best_score": attempts.filter(status='COMPLETED').aggregate(
            max=Max('score')
        )['max']
    }

    serializer = UserAnalyticsSerializer(data)
    return Response(serializer.data)

@extend_schema(
        request=QuizAnalyticsSerializer,
        responses=QuizAnalyticsSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_analytics(request, quiz_id):
    attempts = Attempt.objects.filter(quiz_id=quiz_id)

    total_attempts = attempts.count()
    completed_attempts = attempts.filter(status='COMPLETED').count()

    avg_score = attempts.filter(status='COMPLETED').aggregate(
        avg=Avg('score')
    )['avg']

    completion_rate = (
        (completed_attempts / total_attempts) * 100
        if total_attempts > 0 else 0
    )

    data = {
        "quiz_id": quiz_id,
        "total_attempts": total_attempts,
        "completed_attempts": completed_attempts,
        "average_score": avg_score or 0,
        "completion_rate": completion_rate
    }

    serializer = QuizAnalyticsSerializer(data)
    return Response(serializer.data)