from django.urls import path
from .views import ProductView, ProductDetailView, CategoryListCreateView, CategoryDetailView

app_name = 'products'

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/', CategoryListCreateView.as_view(), name='category'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]