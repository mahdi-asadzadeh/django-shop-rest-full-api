from django.urls import path, include
from comment.api.urls import urlpatterns


app_name = 'comment'

urlpatterns = [
	path('api/', include(urlpatterns)),
]