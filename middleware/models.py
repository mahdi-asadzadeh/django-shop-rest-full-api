from django.db import models


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()

