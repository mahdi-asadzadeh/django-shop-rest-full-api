from django.urls import path
from comment.api import views


urlpatterns = [
	path('create-product/', views.CommentCreateProduct.as_view(), name='comment_create_product'),
	path('create-article/', views.CommentCreateArticle.as_view(), name='comment_create_article'),
	path('update-delete/<int:pk>/', views.CommentUpdateDelete.as_view(), name='comment_update_delete'),
	path('comments-product/<int:pk>/', views.CommentsProduct.as_view(), name='comments-product'),
	path('comments-article/<int:pk>/', views.CommentsArticle.as_view(), name='comments-article'),
]