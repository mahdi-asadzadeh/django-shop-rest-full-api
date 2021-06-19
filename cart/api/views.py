from decimal import Decimal
from rest_framework import serializers, status, generics
from rest_framework.response import Response
from cart.api.serializers import AddToCartSerializer, DeleteCartItemSerializer
from cart.cart import Cart
from product.models import Product


class AddToCart(generics.GenericAPIView):
	serializer_class = AddToCartSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			user = request.user
			product_id = serializer.data['product_id']
			quantity = serializer.data['quantity']

			try:
				product = Product.objects.get(id=product_id)
				Cart.add_to_cart(
					user_id = user.id,
					product_id = product.id,
					product_image = str(product.image.url),
					product_price = str(Decimal(product.price) * quantity),
					product_quantity = quantity,
				)
				content = {'success': 'add to cart.'}
				return Response(content, status=status.HTTP_200_OK)

			except Product.DoesNotExist:
				content = {'error': 'Product matching query does not exist.'}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)
				
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCartItem(generics.GenericAPIView):
	serializer_class = DeleteCartItemSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			row_id = serializer.data['row_id']
			Cart.delete_cart(request.user.id, row_id)
			content = {'success': 'delete cart.'}
			return Response(content, status=status.HTTP_204_NO_CONTENT)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClearCartItem(generics.GenericAPIView):

	def get(self, request):
		Cart.delete_all_carts(self.request.user.id)
		content = {'success': 'clear cart.'}
		return Response(content, status=status.HTTP_204_NO_CONTENT)


class ListCart(generics.GenericAPIView):

	def get(self, request):
		total_price = 0
		items = Cart.carts(request.user.id)
		for item in items:
			total_price += float(item['product_price'])
			
		return Response({
			'items': items,
			'total_price': total_price
		}, status=status.HTTP_200_OK)

