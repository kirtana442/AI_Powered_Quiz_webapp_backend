from rest_framework import serializers
from core.models import Quiz, Question, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Option
        fields = ["id","text", "is_correct"]

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model= Question
        fields = ["id","text","difficulty","points","explanation","options"]

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True,read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Quiz
        fields = ["id","title","topic","difficulty","is_ai_generated","created_by","created_at","questions"]
        read_only_fields = ["created_by","created_at","questions"]

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "quiz", "text", "difficulty", "points", "explanation"]

class OptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "question", "text", "is_correct"]