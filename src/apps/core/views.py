from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

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

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def stock_update(self, request, pk):
        object = self.get_object()
        object.stock = 10
        object.save()
        return Response(status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )
