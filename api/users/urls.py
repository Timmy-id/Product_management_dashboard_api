# users/urls.py
from django.urls import path
# from rest_framework.routers import DefaultRouter

from .views import RegisterView, UserListView

# router = DefaultRouter()
# router.register(r'profile', UserViewSet, basename='user') # 'profile' as endpoint for user details

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', UserListView.as_view(), name='user-list')
]