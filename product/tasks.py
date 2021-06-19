from django.core.cache import cache
from django.conf import settings

from extensions.web_scraping import get_price_gold, get_price_doral
from celery import shared_task
from decimal import Decimal


@shared_task
def run_every_create_gold_price():
    price_gold = get_price_gold()
    price_dolar = get_price_doral()

    if cache.get('gold_rate') == None:
        gold_last = cache.set('gold_rate', round(Decimal(price_gold), 2), settings.TIMEOUT_PRICE_GOLD)

    if cache.get('dolar_rate') == None:
        dolar_last = cache.set('dolar_rate', round(Decimal(price_dolar), 2), settings.TIMEOUT_PRICE_DOLAR)
    
    if price_gold != None:
        cache.set('gold_rate', round(Decimal(price_gold), 2), settings.TIMEOUT_PRICE_GOLD)
    
    if price_dolar != None:
        cache.set('dolar_rate', round(Decimal(price_dolar), 2), settings.TIMEOUT_PRICE_DOLAR)
