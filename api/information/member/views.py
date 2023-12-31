from django.db.models import Count, functions
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import MonthlyJoinSerializer
from .models import Info

import pandas as pd


class MonthlyJoinView(APIView):
    def get(self, request, *args, **kwargs):
        current_month = timezone.now().month
        queryset = Info.objects.values('policy_id').filter(date_joined__month=current_month)
        monthly_join = queryset.count()
        response = {'monthly_join': monthly_join}
        return Response(response, status=status.HTTP_200_OK)


class DailyJoinView(APIView):
    def get(self, request, *args, **kwargs):
        current_date = timezone.now()
        month_ago = current_date - timezone.timedelta(days=30)
        queryset = Info.objects.filter(date_joined__gte=month_ago).annotate(
            date=functions.TruncDate('date_joined')
        ).values('date').annotate(
            daily_count=Count('policy_id')
        ).order_by('date')
        
        try:
            serializer = MonthlyJoinSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except:
            return Response('Somethings went wrong trying to calculating data', status=status.HTTP_400_BAD_REQUEST)