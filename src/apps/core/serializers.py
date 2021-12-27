from django.core.exceptions import ObjectDoesNotExist

from rest_framework_json_api import serializers
from rest_framework.validators import UniqueValidator


from core.models import Product, Order, OrderDetail


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'stock')


class OrderSerializer(serializers.ModelSerializer):
    get_total = serializers.SerializerMethodField(method_name='get_total')
    get_total_usd = serializers.SerializerMethodField(method_name='get_total_usd')

    class Meta:
        model = Order
        fields = ('datetime_register', 'get_total', 'get_total_usd')

    def get_total(self, order):
        return order.get_total()

    def get_total_usd(self, order):
        return order.get_total_usd()
