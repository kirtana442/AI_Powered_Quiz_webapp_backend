from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from core.models import Quiz,Question,Option
from core.serializers.quiz_serializers import QuizSerializer,QuestionCreateSerializer, OptionCreateSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
        request=QuizSerializer,
        responses=QuizSerializer
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_quiz(request):
    if request.user.profile.role != 'ADMIN':
        return Response({"detail": "Only admins can create quizzes"}, status=403)
    
    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        request=QuizSerializer,
        responses=QuizSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_quizzes(request):
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)

@extend_schema(
        request=QuizSerializer,
        responses=QuizSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_detail(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response({"detail": "Quiz not found"}, status=404)
    serializer = QuizSerializer(quiz)
    return Response(serializer.data)

@extend_schema(
        request=QuestionCreateSerializer,
        responses=QuestionCreateSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request):
    if request.user.profile.role != 'ADMIN':
        return Response({"detail": "Only admins can create questions"}, status=403)

    serializer = QuestionCreateSerializer(data=request.data)
    if serializer.is_valid():
        quiz = serializer.validated_data['quiz']

        # extra safety check
        if quiz.created_by != request.user:
            return Response({"detail": "Not your quiz"}, status=403)

        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@extend_schema(
        request=OptionCreateSerializer,
        responses=OptionCreateSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_option(request):
    if request.user.profile.role != 'ADMIN':
        return Response({"detail": "Only admins can create options"}, status=403)

    serializer = OptionCreateSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.validated_data['question']

        # ensure question belongs to admin's quiz
        if question.quiz.created_by != request.user:
            return Response({"detail": "Not your question"}, status=403)

        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

