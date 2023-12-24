from django.urls import path
from .views import MonthlyJoinView


urlpatterns = [
    path('total-member/', MonthlyJoinView.as_view()),
]