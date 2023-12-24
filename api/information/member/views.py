from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import MonthlyJoinSerializer
from .models import Info


class MonthlyJoinView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Info.objects.all()
        serializer = MonthlyJoinSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        