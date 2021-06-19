from django.conf import settings
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from category.models import Category
from .serializers import CategorySerializer
from product.models import Product
from product.api.serializers import ProductListSerializer


class CategoryList(generics.GenericAPIView):
	serializer_class = CategorySerializer

	def get_queryset(self):
		pass

	def get(self, request):
		queryset = None

		if 'categories' in cache:
			queryset = cache.get('categories')
		else:
			queryset = Category.objects.all()
			cache.set('categories', queryset, timeout=settings.TIMEOUT_CATEGORIES)

		serializer = self.serializer_class(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryProducts(generics.GenericAPIView):
	serializer_class = ProductListSerializer
	
	def get_queryset(self):
		pass

	def get(self, request, id, slug):
		category = Category.objects.get(id=id)
		products = category.products.all()
		serializer = self.serializer_class(products, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
