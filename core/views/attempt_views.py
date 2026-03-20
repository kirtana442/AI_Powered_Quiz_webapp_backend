from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from core.models import Attempt, Quiz
from django.shortcuts import get_object_or_404
from core.models import Response as ResponseModel
from core.serializers.response_serializers import SubmitAnswerSerializer
from core.serializers.attempt_serializers import AttemptSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
        request=AttemptSerializer,
        responses=AttemptSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_attempt(request):
    quiz_id = request.data.get('quiz')
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({"detail": "Quiz not found"}, status=404)

    attempt, created = Attempt.objects.get_or_create(
        user=request.user,
        quiz=quiz,
        status='IN_PROGRESS'
    )
    serializer = AttemptSerializer(attempt)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(
        request=AttemptSerializer,
        responses=AttemptSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_attempt(request, pk):
    try:
        attempt = Attempt.objects.get(pk=pk, user=request.user)
    except Attempt.DoesNotExist:
        return Response({"detail": "Attempt not found"}, status=404)

    if attempt.status == 'COMPLETED':
        return Response({"detail": "Attempt already submitted"}, status=400)

    # Calculate score
    total_score = 0
    for response in attempt.responses.all():
        if response.is_correct:
            total_score += response.question.points

    attempt.score = total_score
    attempt.status = 'COMPLETED'
    attempt.end_time = timezone.now()
    attempt.save()

    return Response({"score": total_score}, status=200)

@extend_schema(
        request=AttemptSerializer,
        responses=AttemptSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attempt_history(request):
    attempts = Attempt.objects.filter(user=request.user).order_by('-start_time')
    serializer = AttemptSerializer(attempts, many=True)
    return Response(serializer.data)

@extend_schema(
        request=SubmitAnswerSerializer,
        responses=SubmitAnswerSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request, pk):
    attempt = get_object_or_404(Attempt, pk=pk, user=request.user)

    if attempt.status != 'IN_PROGRESS':
        return Response({"detail": "Attempt already completed"}, status=400)

    serializer = SubmitAnswerSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    question = serializer.validated_data['question']
    option = serializer.validated_data['option']

    if question.quiz_id != attempt.quiz_id:
        return Response({"detail": "Question does not belong to this quiz"}, status=400)

    is_correct = option.is_correct

    response_obj, created = ResponseModel.objects.update_or_create(
        attempt=attempt,
        question=question,
        defaults={
            "selected_option": option,
            "is_correct": is_correct
        }
    )

    return Response({
        "question_id": question.id,
        "selected_option": option.id,
        "is_correct": is_correct,
        "message": "Answer saved" if created else "Answer updated"
    }, status=200)