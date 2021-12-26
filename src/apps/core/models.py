import uuid
from django.db import models
from django.utils import timezone


from json import JSONEncoder
from uuid import UUID

JSONEncoder_olddefault = JSONEncoder.default

def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)

JSONEncoder.default = JSONEncoder_newdefault


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=250)
    price = models.FloatField(null=False, blank=False)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return f"{self.stock} - {self.name}"


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    datetime_register = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("datetime_register", )

    def __str__(self):
        return f"{self.id} ({self.datetime_register})"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cuantity = models.PositiveIntegerField()

    class Meta:
        ordering = ("order", "product")
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='order_product_unique')
        ]