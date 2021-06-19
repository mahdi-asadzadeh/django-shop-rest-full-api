from django.db.models import Count
from django.utils.text import slugify

from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer
from rest_framework import serializers

from category.models import Category
from product.models import Product, GalleryProduct, Stone, Color, Size
from category.api.serializers import CategorySerializer
from extensions.calculations import calculating_gold_jewelry
from taggit_serializer.serializers import (
	TagListSerializerField,
	TaggitSerializer
	)


def _create_custom_uuid():
	max_id = 1
	ex_last_product = Product.objects.last()
	if ex_last_product:
		max_id = ex_last_product.id

	my_id = '{}{:07d}'.format('EUA', max_id if max_id is not None else 1)
	return my_id


class ColorSerializer(ModelSerializer):
	class Meta:
		model = Color
		fields = ['id', 'color']


class SizeSerializer(ModelSerializer):
	class Meta:
		model = Size
		fields = ['id', 'size']


class StoneSerilizer(ModelSerializer):
	class Meta:
		model = Stone
		fields = '__all__'
		

class ImageCreateProductSerializer(serializers.Serializer):
	class Meta:
		model = GalleryProduct
		fields = ['image']
	

class ProductListSerializer(serializers.ModelSerializer):
	gallery = serializers.SerializerMethodField()
	category = serializers.SerializerMethodField()
	price = serializers.SerializerMethodField()

	class Meta:
		model = Product
		fields = [
			'id',
			'rating',
			'title',
			'slug',
			'image',
			'gallery',
			'category',
			'price'
		]

	def get_category(self, obj):
		result = obj.category
		return CategorySerializer(instance=result).data

	def get_gallery(self, obj):
		result = GalleryProduct.objects.filter(product_id=obj)
		return ImageProductSerializer(instance=result, many=True).data

	def get_price(self, obj):
		return obj.price


class ProductsOrderCartSerializer(ModelSerializer):

	class Meta:
		model = Product
		fields = ['id', 'title', 'slug', 'image']


class ProductDetailSerializer(TaggitSerializer, ModelSerializer):
	tags = TagListSerializerField()
	gallery = SerializerMethodField()
	color = SerializerMethodField()
	size = SerializerMethodField()
	category = SerializerMethodField()
	price = serializers.SerializerMethodField()

	class Meta:
		model = Product
		exclude = [
			'site_rate',
			'is_rate_fixed',
			'provider_gold_rate',
			'provider_diamond_price',
		]

	def get_color(self, obj):
		result = obj.color.all()
		return ColorSerializer(instance=result, many=True).data

	def get_size(self, obj):
		result = obj.size.all()
		return SizeSerializer(instance=result, many=True).data

	def get_category(self, obj):
		return CategorySerializer(instance=obj.category).data

	def get_gallery(self, obj):
		result = GalleryProduct.objects.filter(product_id=obj)
		return ImageProductSerializer(instance=result, many=True).data

	def get_price(self, obj):
		return obj.price


class ImageProductSerializer(ModelSerializer):
	class Meta:
		model = GalleryProduct
		fields = ['image', 'product']
