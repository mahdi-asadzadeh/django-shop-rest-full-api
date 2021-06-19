from rest_framework.serializers import ModelSerializer, SerializerMethodField
from category.models import Category
from product.models import Product


class CategoryNavbarSerializer(ModelSerializer):
	category_child = SerializerMethodField()
	product = SerializerMethodField()

	class Meta:
		model = Category
		fields = ['id', 'name', 'slug', 'product']

	def get_product(self, obj):
		product = Product.objects.order_by('-create').filter(category_material=obj)[:1]
		return ProductListSerializer(instance=product, many=True).data


class CategorySerializer(ModelSerializer):

	class Meta:
		model = Category
		fields = ['id', 'name', 'slug']
