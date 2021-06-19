from django.core.cache import cache
from django.conf import settings

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, generics

from blog.models import Article
from blog.api.serializers import (
	ArticleDetailSerializer,
	ArticleListSerializer,
)


class SetPagination(PageNumberPagination):
	page_size = settings.ARTICLES_PAGINATION
	page_size_query_param = 'page_size'
	max_page_size = settings.MAX_ARTICLES_PAGINATION


class ArticleList(ListAPIView):
	ordering_fields = ['create', 'hits', 'rating']
	serializer_class = ArticleListSerializer
	pagination_class = SetPagination
	search_fields = [
		'name',
		'slug',
		'body',
		'tags__name',
		'tags__name',
		'body'
	]
	def get_queryset(self):
		if 'articles' in cache:
			articles = cache.get('articles')
			return articles
		else:
			queryset =  Article.objects.filter(status='p')
			cache.set('articles', queryset, timeout=settings.TIMEOUT_ARTICLES)
			return queryset


class ArticleDetail(generics.GenericAPIView):
	serializer_class = ArticleDetailSerializer

	def get(self, request, slug, pk):
		try:
			queryset = Article.objects.get(pk=pk, status='p')
			queryset.hits += 1
			queryset.save()
			serializer = self.serializer_class(queryset).data
			return Response(serializer, status=status.HTTP_200_OK)

		except Exception:
			return Response(status=status.HTTP_404_NOT_FOUND)
