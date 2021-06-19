from django.urls import path
from .views import ProductList, ProductDetail


app_name = 'products'

urlpatterns = [
    path('product-list/', ProductList.as_view(), name='product_list'),
    path('product-detail/<slug:slug>/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
]
