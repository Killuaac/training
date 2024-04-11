from django.db import models

from ..entrance.models import CustomUser


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.email


class Order(models.Model):
    product = models.ManyToManyField(Product)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.user.email