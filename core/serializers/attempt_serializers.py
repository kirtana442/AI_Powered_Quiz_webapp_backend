from rest_framework import serializers
from core.models import Attempt, Response

class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = ["id","quiz","status","score","start_time","end_time"]
        read_only_fields = ["status","score","start_time","end_time"]