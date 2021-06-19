"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from .yasg import schema_view


urlpatterns = [
	path('admin/', admin.site.urls),
	re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   	path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
	  
	path('cart/', include('cart.urls')),
	path('order/', include('order.urls')),
	path('blog/', include('blog.urls')),
	path('category/', include('category.urls')),
	path('product/', include('product.urls')),
	path('accounts/', include('accounts.urls')),
	path('comment/', include('comment.urls')),
	path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG == True:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
