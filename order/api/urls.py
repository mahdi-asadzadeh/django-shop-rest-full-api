from django.urls import path
from order.api import views


urlpatterns = [
	# path('to-bank/<int:order_id>/', views.ToBank.as_view()),
	# path('verify/', views.Verify.as_view()),
	path('order-list/', views.OrderList.as_view()),
	path('order-create/', views.OrderCreate.as_view(), name='create_order'),
	path('order-detail/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
]