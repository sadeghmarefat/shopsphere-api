from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = ('id', 'name','owner', 'category', 'description', 'price', 'stock','created_at','updated_at')
        read_only_fields = ('created_at', 'updated_at','id','owner')
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name','slug','created_at','updated_at')
        read_only_fields = ('created_at', 'updated_at','id')