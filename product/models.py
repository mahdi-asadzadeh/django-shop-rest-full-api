import os

from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.utils.html import format_html
from django.core.cache import cache
from django.db import models


from extensions.calculations import calculating_gold_jewelry
from taggit.managers import TaggableManager
from category.models import Category


def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_gallery_image_path(instance, filename):
	name, ext = get_filename_ext(filename)
	try:
		latest_id = Product.objects.latest('pk').id
	except Product.DoesNotExist:
		latest_id = 0
	latest_id +=1
	final_name = f"{instance.slug}-{latest_id}-{ext}"
	return f"products/images/image/{final_name}"


class Size(models.Model):
	size = models.PositiveIntegerField()


class Color(models.Model):
	color = models.CharField(unique=True, max_length=30)


class Product(models.Model):
	CHOICES_STATUS = (
		('r', 'return'),
		('p', 'publish'),
		('d', 'draft')
		)
	CHOICES_CARAT = (
		("24", "24 ayar"),
		("22", "22 ayar"),
		("18", "18 ayar"),
		("14", "14 ayar"),
		("8", "8 ayar"),
		)
	title = models.CharField(max_length=50)
	slug = models.SlugField(unique=True, allow_unicode=True, max_length=100)

	color = models.ManyToManyField(Color)
	size = models.ManyToManyField(Size, blank=True)
	carat = models.CharField(choices=CHOICES_CARAT, max_length=2)
	weight = models.DecimalField(max_digits=6, decimal_places=3)
	length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')

	site_rate = models.DecimalField(max_digits=3, decimal_places=3, null=True, blank=True)

	# True = gold  |  False = jewelry
	gold_or_jewelry = models.BooleanField(verbose_name='Is gold ?')

	# if be gold
	is_rate_fixed = models.BooleanField(default=False)
	provider_gold_rate = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)

	# if be jewelry
	provider_diamond_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

	body = models.TextField()
	iframe = models.TextField(null=True, blank=True)
	status = models.CharField(choices=CHOICES_STATUS, max_length=1)
	create = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)
	image = models.ImageField(upload_to=upload_gallery_image_path)
	
	numbers_rating = models.FloatField(default=0)
	scope_avrage = models.FloatField(default=0)
	rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
	
	tags = TaggableManager()


	def image_tag(self):
		return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.image.url))

	def __str__(self):
		return f'{self.title} - {self.id}'
	
	@property
	def get_tags(self):
		return self.tags.all()

	@property
	def price(self):
		return calculating_gold_jewelry(self)

	@property
	def visit(self):
		settings.REDIS.hsetnx('product_visit', self.id, 0)
		return settings.REDIS.hget('product_visit', self.id)

	class Meta:
		ordering = ['-create']


class Stone(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=50)
	size = models.DecimalField(max_digits=4, decimal_places=2)
	color = models.CharField(max_length=50)
	clarity = models.CharField(max_length=50)
	cut = models.CharField(max_length=50)
	quantity = models.IntegerField()


class GalleryProduct(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='galleries')
	image = models.ImageField(upload_to='products/gallery/')
