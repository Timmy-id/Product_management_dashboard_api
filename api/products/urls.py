# users/urls.py
from django.urls import path

from .views import create_product, list_products, update_product, delete_product

app_name = 'products'

urlpatterns = [
    path('', create_product, name='create_product'),
    path('list_products/', list_products, name='list_products'),
    path('<str:pk>/', update_product, name='update_product'),
    path('<str:pk>/', delete_product, name='delete_product'),
]