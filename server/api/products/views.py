from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer
from .models import Product


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    user = request.user
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)

    if product.owner != user:
        return Response({'error': 'You are not the owner of this product'}, status=status.HTTP_403_FORBIDDEN)
    serializer = ProductSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    try:  
        user = request.user
        product = Product.objects.get(id=pk)

        if product.owner != user:
            return Response({'error': 'You are not the owner of this product'}, status=status.HTTP_403_FORBIDDEN)
    except product.DoesNotExist:
        return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    product.delete()
    return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)