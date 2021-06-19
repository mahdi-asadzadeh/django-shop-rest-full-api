from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(allow_unicode=True, unique=True, max_length=50)

    def __str__(self):
        return f'{self.name} - {self.slug}'

    class Meta:
        verbose_name = 'Level 2'
        verbose_name_plural = 'Level 2'
