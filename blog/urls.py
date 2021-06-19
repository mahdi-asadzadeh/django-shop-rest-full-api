from django.urls import path, include
from blog.api.urls import urlpatterns


app_name = 'blog'

urlpatterns = [
	path('api/', include(urlpatterns)),
]