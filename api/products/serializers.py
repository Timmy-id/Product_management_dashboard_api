from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Product

User = get_user_model()


class SimpleOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class ProductSerializer(serializers.ModelSerializer):
    owner = SimpleOwnerSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'owner', 'name', 'slug', 'description', 'price', 'is_available', 'stock_quantity', 'product_image', 'created_at', 'updated_at']
