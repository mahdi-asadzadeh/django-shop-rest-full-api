from rest_framework.reverse import reverse
from rest_framework import serializers
from blog.models import Article


class ArticleListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		exclude = ['status', 'body', 'numbers_rating', 'scope_avrage']


class ArticleDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = Article
		exclude = ['status', 'numbers_rating', 'scope_avrage']
