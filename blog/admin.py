from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'user', 'status', 'image_tag')
	list_filter = ('status',)
	search_fields = ('name', 'slug', 'body')
	prepopulated_fields = {'slug': ('name',)}
