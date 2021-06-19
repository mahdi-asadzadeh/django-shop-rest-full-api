from django.urls import path
from .views import CategoryList, CategoryProducts


urlpatterns = [
    path('category-list/', CategoryList.as_view(), name='category_list'),
    path('category-product/<int:id>/<slug:slug>/', CategoryProducts.as_view(), name='category_product')
]
