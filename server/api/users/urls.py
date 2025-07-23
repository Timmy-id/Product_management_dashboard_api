# users/urls.py
from django.urls import path

from .views import register_user, update_user_profile

app_name = 'users'

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('/update_profile', update_user_profile, name='update_user_profile'),
]