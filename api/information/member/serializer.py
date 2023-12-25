from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Info


class MonthlyJoinSerializer(ModelSerializer):
    date_joined = serializers.CharField(max_length=10)
    policy_id = serializers.CharField(max_length=10)
    
    class Meta:
        model = Info
        fields = [
            'date_joined',
            'policy_id',
        ]