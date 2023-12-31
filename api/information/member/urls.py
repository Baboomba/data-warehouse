from django.urls import path
from .views import MonthlyJoinView, DailyJoinView


urlpatterns = [
    path('total-member/', MonthlyJoinView.as_view()),
    path('monthly-join/', DailyJoinView.as_view()),
]