from rest_framework.routers import DefaultRouter

from core.views import ProductViewSet, OrderViewSet, OrderDetailViewSet


router = DefaultRouter()

router.register('product', ProductViewSet, basename='product')
router.register('order', OrderViewSet, basename='order')
router.register('orderdetail', OrderDetailViewSet, basename='orderdetail')
