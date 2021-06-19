from django.core.cache import cache
from django.conf import settings

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status

from product.models import Product
from .serializers import (
	ProductListSerializer, 
	ProductDetailSerializer, 
)


class SetPagination(PageNumberPagination):
    page_size = settings.PRODUCTS_PAGINATION
    page_size_query_param = 'page_size'
    max_page_size = settings.MAX_PRODUCTS_PAGINATION


class ProductList(ListAPIView):
	pagination_class = SetPagination
	serializer_class = ProductListSerializer

	def get_queryset(self):
		if 'products' in cache:
			products = cache.get('products')
			return products
		else:
			products = Product.objects.filter(status='p')
			cache.set('products', products, timeout=settings.TIMEOUT_PRODUCTS)
			return products

	filterset_fields = [
		'color__color',
		'size__size',
		'gold_or_jewelry',
	]
	search_fields = [
		'title',
		'slug',
		'category__name',
		'category__slug',
		'body',
		'tags__name',
		'tags__slug',
	]
	ordering_fields = [
		'create',
		'rating',
	]			


class ProductDetail(GenericAPIView):
	serializer_class = ProductDetailSerializer

	def get(self, request, slug, pk):
		try:
			queryset = Product.objects.get(pk=pk, status="p")
			serializer = self.serializer_class(queryset).data
			related_contents = queryset.tags.similar_objects()[:15]
			related_contents = ProductListSerializer(instance=related_contents, many=True).data
			return Response({'product': serializer, 'related_contents': related_contents})

		except Product.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
