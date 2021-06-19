from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models

from .managers import CommentManager


User = get_user_model()


class Comment(models.Model):
    RATE_CHOICES = (
        ('5', 'excellent'),
        ('4', 'very good'),
        ('3', 'good'),
        ('2', 'bad'),
        ('1', 'very bad')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    full_name = models.CharField(max_length=20, null=True, blank=True)
    rate = models.CharField(choices=RATE_CHOICES, max_length=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="post")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    body = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email

    objects = CommentManager()
