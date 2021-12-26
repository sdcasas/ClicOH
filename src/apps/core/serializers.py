from django.core.exceptions import ObjectDoesNotExist

from rest_framework_json_api import serializers
from rest_framework.validators import UniqueValidator


from core.models import Product, Order, OrderDetail


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(min_value=0, default=0)

    class Meta:
        model = Product
        fields = ('name', 'price', 'stock')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('datetime_register', )
