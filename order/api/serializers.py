from rest_framework import serializers
from order.models import (
	Order,
	OrderItem,
)
from product.api.serializers import ProductsOrderCartSerializer


class CompareAddSerializer(serializers.Serializer):
	product_id = serializers.IntegerField(required=True)


class OrderUpdateRemittance(serializers.Serializer):
	image = serializers.ImageField()
	pk = serializers.IntegerField()


class OrderAdvertisingSerializer(serializers.ModelSerializer):
	advertising_id = serializers.IntegerField()
	proposal_provider_id = serializers.IntegerField()

	class Meta:
		model = Order
		exclude = [
			'size',
			'color',
			'is_advertising',
			'user',
			'email',
			'create',
			'update',
			'paid',
			'total_price',
			'accepted',
			'posted',
			'order_code',
			'provider',
			'authority'
		]


class OrderSerializer(serializers.Serializer):
	address = serializers.CharField(max_length=200)


class OrderListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
	products = serializers.SerializerMethodField()

	class Meta:
		model = Order
		exclude = ['user']

	def get_products(self, obj):
		result = OrderItem.objects.filter(order_id=obj)
		return OrderItemSerializer(instance=result, many=True).data


class OrderItemSerializer(serializers.ModelSerializer):
	product = serializers.SerializerMethodField()
	size = serializers.SerializerMethodField()
	color = serializers.SerializerMethodField()

	class Meta:
		model = OrderItem
		fields = '__all__'

	def get_product(self, obj):
		result = obj.product
		return ProductsOrderCartSerializer(instance=result).data
