from django.urls import path
from .views import SignUpView, HTTPOnlyLoginView, ReadUserView, HTTPOnlyLogoutView


urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('login/', HTTPOnlyLoginView.as_view()),
    path('users/', ReadUserView.as_view()),
    path('logout/', HTTPOnlyLogoutView.as_view()),
]