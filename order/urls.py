from django.urls import path, include
from order.api.urls import urlpatterns


app_name = 'order'

urlpatterns = [
	path('api/', include(urlpatterns)),
]
