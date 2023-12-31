from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Info


class MonthlyJoinSerializer(ModelSerializer):
    date = serializers.DateField()
    daily_count = serializers.IntegerField()
    
    class Meta:
        model = Info
        fields = [
            'date',
            'daily_count',
        ]