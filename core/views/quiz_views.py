from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from core.models import Quiz,Question,Option
from core.serializers.quiz_serializers import QuizSerializer,QuestionCreateSerializer, OptionCreateSerializer
from drf_spectacular.utils import extend_schema

from django.db import transaction
from core.models import AIRequest
from core.utils import generate_quiz_questions
import random
import time

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

@extend_schema(
    responses={200: None}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_quiz_ai(request, pk):
    
    if request.user.profile.role != 'ADMIN':
        return Response({"detail": "Only admins can generate quizzes"}, status=403)

    
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response({"detail": "Quiz not found"}, status=404)

    
    if quiz.created_by != request.user:
        return Response({"detail": "Not your quiz"}, status=403)

    MAX_RETRIES = 3
    RETRY_DELAY = 1
    last_error = None

    for attempt_num in range(1, MAX_RETRIES + 1):

        ai_request = AIRequest.objects.create(
            user=request.user,
            topic=quiz.topic,
            difficulty=quiz.difficulty,
            num_questions=quiz.questions.count() or 5,
            status="PENDING"
        )

        try:
            
            data = generate_quiz_questions(
                ai_request.topic,
                ai_request.num_questions,
                ai_request.difficulty
            )

            
            if not isinstance(data, list):
                raise ValueError("Invalid AI response format")

            with transaction.atomic():

                
                quiz.questions.all().delete()

                seen_questions = set()

                for q in data:

                    
                    if q["question"] in seen_questions:
                        continue
                    seen_questions.add(q["question"])

                    question = Question.objects.create(
                        quiz=quiz,
                        text=q["question"],
                        difficulty=q.get("difficulty"),
                        explanation=q.get("explanation", ""),
                        points=1
                    )

                    options = q["options"]

                    
                    correct_count = sum(
                        1 for opt in options if opt.get("is_correct") is True
                    )

                    if correct_count != 1:
                        raise ValueError(
                            f"Invalid options for question: {q['question']}"
                        )

                    
                    random.shuffle(options)

                    for opt in options:
                        Option.objects.create(
                            question=question,
                            text=opt["text"],
                            is_correct=opt["is_correct"]
                        )

                
                quiz.is_ai_generated = True
                quiz.save()

                
                ai_request.response_json = data
                ai_request.status = "SUCCESS"
                ai_request.save()

            return Response({
                "message": "Quiz generated successfully",
                "questions_created": len(seen_questions),
                "attempts_used": attempt_num
            }, status=200)

        except Exception as e:
            ai_request.status = "FAILED"
            ai_request.error_message = str(e)
            ai_request.save()

            last_error = str(e)

            if attempt_num < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt_num)
            else:
                break

    
    return Response(
        {
            "error": "AI generation failed after multiple attempts",
            "details": last_error,
            "suggestion": "Try again later or create quiz manually"
        },
        status=503
    )