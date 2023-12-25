from django.urls import path
from .views import TotalMemberView, MonthlyJoinView


urlpatterns = [
    path('total-member/', TotalMemberView.as_view()),
    path('monthly-join/', MonthlyJoinView.as_view()),
]