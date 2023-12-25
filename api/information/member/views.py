from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import MonthlyJoinSerializer
from .models import Info

import pandas as pd


class TotalMemberView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Info.objects.all()
        monthly_join = queryset.count()
        response = {'monthly_join': monthly_join}
        return Response(response, status=status.HTTP_200_OK)


class MonthlyJoinView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Info.objects.values('date_joined', 'policy_id')
                
        try:
            df = pd.DataFrame(queryset)
            df['date_joined'] = pd.to_datetime(df['date_joined']).dt.to_period('M')
            df = df.groupby('date_joined')['policy_id'].count().reset_index()
            df = df.iloc[-12:, :]
            df['date_joined'] = df['date_joined'].dt.strftime('%Y-%m')
            data = df.to_dict(orient='records')
            serializer = MonthlyJoinSerializer(data, many=True)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except:
            return Response('Somethings went wrong trying to calculating data', status=status.HTTP_400_BAD_REQUEST)