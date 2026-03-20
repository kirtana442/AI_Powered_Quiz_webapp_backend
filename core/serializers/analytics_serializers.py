from rest_framework import serializers

class UserAnalyticsSerializer(serializers.Serializer):
    total_attempts = serializers.IntegerField()
    completed_attempts = serializers.IntegerField()
    in_progress_attempts = serializers.IntegerField()
    average_score = serializers.FloatField()
    best_score = serializers.IntegerField(allow_null=True)


class QuizAnalyticsSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    total_attempts = serializers.IntegerField()
    completed_attempts = serializers.IntegerField()
    average_score = serializers.FloatField()
    completion_rate = serializers.FloatField()