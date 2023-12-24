from rest_framework.serializers import ModelSerializer
from .models import Info


class MonthlyJoinSerializer(ModelSerializer):
    
    class Meta:
        model = Info
        fields = [
            'policy_id',
            'date_joined'
        ]      