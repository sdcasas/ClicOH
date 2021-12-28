from .models import Product, Order, OrderDetail
from .serializers import ProductSerializer, OrderSerializer, OrderDetailSerializer

from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Prefetch
from django.conf import settings
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        stock = serializer.validated_data.get('stock', 0)
        if stock <= 0:
            raise ValidationError('El campo stock debe ser mayor a cero (0)')
        serializer.save()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save()


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated, )

    def validate_cuantity(self, serializer):
        product = serializer.validated_data.get('product', None)
        cuantity = serializer.validated_data.get('cuantity', 0)
        if cuantity == 0:
            raise ValidationError('El campo cuantity debe ser mayor a cero (0).')
        if cuantity > product.stock:
            raise ValidationError(f'El producto {product.name} no tiene suficiente stock. '
                                  f'Stock actual: {product.stock}')

    def validate_product(self, serializer):
        order = serializer.validated_data.get('order', None)
        product = serializer.validated_data.get('product', None)
        if order.details.filter(product=product).exists():
            raise ValidationError(f'El product {product.name} ya se encuentra cargado')

    def stock_update(self, serializer):
        product = serializer.validated_data.get('product', None)
        cuantity = serializer.validated_data.get('cuantity', 0)
        product.stock = product.stock - cuantity
        product.save()

    def perform_create(self, serializer):
        self.validate_cuantity(serializer)
        self.validate_product(serializer)
        serializer.save()
        self.stock_update(serializer)

    def perform_destroy(self, instance):
        product = instance.product
        product.stock += instance.cuantity
        instance.delete()
        product.save()
