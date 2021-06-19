from django.urls import path
from cart.api import views


urlpatterns = [
    path('add_to_cart/', views.AddToCart.as_view(), name='add_to_cart'),
    path('delete_cart/', views.DeleteCartItem.as_view(), name='delete_cart'),
    path('clear_cart/', views.ClearCartItem.as_view(), name='clear_cart'),
    path('list_cart/', views.ListCart.as_view(), name='list_cart'),
]
