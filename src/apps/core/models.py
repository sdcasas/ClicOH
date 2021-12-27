import uuid
from django.db import models
from django.utils import timezone

from core.utils import get_dolar_blue


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

    def get_total(self):
        total = 0
        for orderdetail in self.details.all():
            total += orderdetail.product.price * orderdetail.cuantity
        return total

    def get_total_usd(self):
        dolar_blue_value = get_dolar_blue()
        if dolar_blue_value:
            return self.get_total() / dolar_blue_value
        else:
            return None


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cuantity = models.PositiveIntegerField()

    class Meta:
        ordering = ("order", "product")
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='order_product_unique')
        ]