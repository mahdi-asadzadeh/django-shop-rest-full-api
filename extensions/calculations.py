from django.db.models import Count
from django.core.cache import cache

from decimal import Decimal


def calculating_gold_jewelry(product):
	
	dolar_price = cache.get('dolar_rate')
	gold_price = cache.get('gold_rate')

	if dolar_price == None:
		dolar_price = 1000

	if gold_price == None:
		gold_price = 1000
		

	price = None

	carat = product.carat
	a = Decimal(carat) / 24

	if product.site_rate == None:
		product.site_rate = product.provider_gold_rate

	if product.gold_or_jewelry == True:
		is_rate_fixed = product.is_rate_fixed
		provider_gold_rate = product.provider_gold_rate

		if is_rate_fixed == True:
			b = Decimal(a) + Decimal(product.site_rate)
			c = Decimal(b) * Decimal(product.weight)
			e = Decimal(c) * Decimal(gold_price)
			price = Decimal(e) + Decimal(product.provider_gold_rate)
		else:
			b = Decimal(a) + Decimal(product.site_rate)
			c = Decimal(b) + Decimal(product.provider_gold_rate)
			d = Decimal(c) * Decimal(product.weight)
			price = Decimal(d) * Decimal(gold_price)
	else:
		if product.site_rate == None:
			product.site_rate = (product.provider_diamond_price * 15) / 100

		a = Decimal(product.provider_diamond_price) + Decimal(product.site_rate)
		price = Decimal(a) * Decimal(dolar_price)

	return round(price, 2)
