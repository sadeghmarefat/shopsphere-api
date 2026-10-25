from django.shortcuts import render
from rest_framework import generics
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .permissions import IsOwnerOrReadOnly

# Create your views here.



class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('-name')
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUser()]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUser()]