import datetime
from zeep import Client
from django.utils import timezone

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from order.api.serializers import (
	OrderSerializer,
	OrderDetailSerializer,
	OrderListSerializer,
	)
from product.models import Product
from order.models import (
	Order,
	OrderItem,
)
from cart.cart import Cart


def create_custom_uuid():
	try:
		max_id = Order.objects.latest('pk').id
	except Order.DoesNotExist:
		max_id = 1
	my_id = "{}{:08d}".format('ODR', max_id if max_id is not None else 1)
	return my_id


# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# description = 'توضیحات مربوط به تراکنش را در این قسمت وارد کنید'  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.
#
#
# class ToBank(GenericAPIView):
# 	permission_classes = [IsAuthenticated, ]
#
# 	def get(self, request, order_id):
#
# 		try:
# 			order = Order.objects.get(pk=order_id)
# 		except Exception:
# 			return Response(status=status.HTTP_404_NOT_FOUND)
#
# 		amount = order.total_price
# 		result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
# 		if result.Status == 100 and len(result.Authority) == 36:
# 			star_pay_url = ''
# 			authority = str(result.Authority)
# 			order.authority = authority
# 			order.save()
# 			return HttpResponseRedirect(redirect_to=f'{star_pay_url}{authority}')
#
# 		else:
# 			content = {'detail': str(result.Status)}
# 			return Response(content, status=status.HTTP_400_BAD_REQUEST)
#
#
# class Verify(GenericAPIView):
# 	permission_classes = [IsAuthenticated, ]
#
# 	def get(self, request):
# 		if request.GET.get('Status') == 'OK':
# 			authority = request.GET['Authority']
# 			order = Order.objects.get(authority=authority)
# 			amount = order.total_price
# 			result = client.service.PaymentVerification(MERCHANT, authority, amount)
# 			if result.Status == 100:
# 				order.paid = True
# 				order.save()
# 				return Response(status=status.HTTP_200_OK)
# 			else:
# 				order.delete()
# 				content = {'detail': 'Transaction failed.'}
# 				return Response(content, status=status.HTTP_400_BAD_REQUEST)
# 		else:
# 			content = {'detail': 'Transaction failed or canceled by user.'}
# 			return Response(content, status=status.HTTP_400_BAD_REQUEST)


class OrderCreate(GenericAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = OrderSerializer
	
	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			address = serializer.data['address']
			user = request.user
			carts = Cart.carts(user.id)
			if carts == []:
				content = {'error': 'carts are empty.'}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)
			total_price = 0
			for cart in carts:
				total_price += float(cart['product_price'])
			order = Order.objects.create(
				user=user,
				price=total_price,
				paid=False,
				address=address,
				)
			for cart in carts:
				OrderItem.objects.create(
					product=Product.objects.get(id=cart['product_id']),
					order=order,
				)
			Cart.delete_all_carts(user.id)
			content = {'success': 'create order.'}
			return Response(content, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderList(GenericAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = OrderListSerializer
	
	def get_queryset(self, request):
		orders = Order.objects.filter(user=request.user)
		serializer = self.serializer_class(orders, many=True).data
		return Response(serializer, status=status.HTTP_200_OK)


class OrderDetail(GenericAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = OrderDetailSerializer

	def get_queryset(self, request, pk):
		try:
			queryset = Order.objects.get(user=request.user, pk=pk)
			serializer = self.serializer_class(instance=queryset).data
			return Response(serializer, status=status.HTTP_200_OK)

		except Exception:
			return Response(status=status.HTTP_404_NOT_FOUND)
