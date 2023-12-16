from django.urls import path
from .views import SignUpView, HTTPOnlyLoginView, ReadUserView


urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('login/', HTTPOnlyLoginView.as_view()),
    path('users/', ReadUserView.as_view()),
]