from datetime import datetime

from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User

import datetime


class Product(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=100, default=29.99)
    image = models.FileField(upload_to="store/img", blank=True, null=True)
    quantity = models.IntegerField(default=1)


    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    count = models.PositiveIntegerField(default=0)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User: {} has {} items in their cart. Their total is ${}".format(self.user, self.count, self.total)


class Entry(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=CASCADE)
    cart = models.ForeignKey(Cart, null=True, on_delete=CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "This entry contains {} {}(s).".format(self.quantity, self.product.name)


@receiver(post_save, sender=Entry)
def update_cart(sender, instance, **kwargs):
    line_cost = instance.quantity * instance.product.cost
    instance.cart.total += line_cost
    instance.cart.count += instance.quantity
    instance.cart.updated = datetime.now()