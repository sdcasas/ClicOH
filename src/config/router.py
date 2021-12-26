from rest_framework.routers import DefaultRouter

from core.views import ProductViewSet, OrderViewSet


router = DefaultRouter()

router.register('product', ProductViewSet, basename='product')
router.register('order', OrderViewSet, basename='order')
