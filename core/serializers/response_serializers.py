from rest_framework import serializers
from core.models import Question, Option

class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    def validate(self, data):
        try:
            question = Question.objects.get(id=data['question_id'])
        except Question.DoesNotExist:
            raise serializers.ValidationError("Invalid question_id")

        try:
            option = Option.objects.get(id=data['option_id'])
        except Option.DoesNotExist:
            raise serializers.ValidationError("Invalid option_id")

        # Ensure option belongs to question
        if option.question_id != question.id:
            raise serializers.ValidationError("Option does not belong to question")

        data['question'] = question
        data['option'] = option

        return data