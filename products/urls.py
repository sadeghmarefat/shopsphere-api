from django.urls import path
from .views import ProductView, ProductDetailView

app_name = 'products'

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]