from django.urls import path
from blog.api.views import ArticleDetail, ArticleList

app_name = 'blog'

urlpatterns = [
	path('article-detail/<str:slug>/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
	path('article-list/', ArticleList.as_view(), name='article_list'),
]