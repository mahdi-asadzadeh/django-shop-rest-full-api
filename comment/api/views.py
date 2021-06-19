from django.contrib.contenttypes.models import ContentType

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from comment.api.serializers import CommentCreateSerializer, CommentSerializer
from product.models import Product
from blog.models import Article
from comment.models import Comment
from order.models import Order


class CommentsProduct(GenericAPIView):
	serializer_class = CommentSerializer

	def get_queryset(self):
		pass

	def get(self, request, pk):
		try:
			product = Product.objects.get(id=pk)
			queryset = Comment.objects.filter_by_instance(product)
			result = self.serializer_class(instance=queryset, many=True).data
			return Response(result)
		except Product.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)


class CommentsArticle(GenericAPIView):
	serializer_class = CommentSerializer
	
	def get_queryset(self):
		pass

	def get(self, request, pk):
		try:
			article = Article.objects.get(id=pk)
			queryset = Comment.objects.filter_by_instance(article)
			result = self.serializer_class(instance=queryset, many=True).data
			return Response(result)

		except Article.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)


class CommentCreateProduct(GenericAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = CommentCreateSerializer
	
	def post(self, request, format=None):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			try:
				product = Product.objects.get(pk=serializer.data['object_id'])
				comment_for_model = ContentType.objects.get_for_model(Product)
				comment = Comment.objects.create(
					user=request.user,
					content_type=comment_for_model,
					object_id=product.id,
					rate=serializer.data['rate'],
					body=serializer.data['body'],
					)
				product.numbers_rating += 1
				product.scope_avrage += int(serializer.data['rate'])
				product.rating = product.scope_avrage / product.numbers_rating
				product.save()
				
				return Response(status=status.HTTP_201_CREATED)

			except Exception:
				return Response(status=status.HTTP_404_NOT_FOUND)

		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CommentCreateArticle(GenericAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = CommentCreateSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			try:
				article = Article.objects.get(pk=serializer.data['object_id'])
				comment_for_model = ContentType.objects.get_for_model(Article)
				Comment.objects.create(
					full_name=serializer.data['full_name'],
					user=request.user,
					content_type=comment_for_model,
					object_id=article.id,
					body=serializer.data['body'],
					rate=serializer.data['rate'],
				)
				article.numbers_rating += 1
				article.scope_avrage += int(serializer.data['rate'])
				numbers_rating = article.numbers_rating
				scope_avrage = article.scope_avrage
				rating = scope_avrage / numbers_rating
				article.rating = rating
				article.save()
				return Response(status=status.HTTP_201_CREATED)

			except:
				return Response(status=status.HTTP_404_NOT_FOUND)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateDelete(GenericAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = CommentSerializer

	def get_queryset(self):
		pass
	
	def put(self, request, pk):
		try:
			comment = Comment.objects.get(pk=pk, user=request.user)
			serializer = self.serializer_class(instance=comment, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)

			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		except Comment.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

	def delete(self, request, pk):
		try:
			comment = Comment.objects.get(pk=pk, user=request.user)
			comment.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)

		except Comment.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
