from django.urls import path, include
from cart.api.urls import urlpatterns


app_name = 'cart'

urlpatterns = [
	path('api/', include(urlpatterns)),
]
