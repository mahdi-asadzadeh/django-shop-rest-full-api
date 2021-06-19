from django.db import models
from django.contrib.auth import get_user_model

from product.models import Product


User = get_user_model()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    authority = models.CharField(null=True, blank=True, max_length=100)
