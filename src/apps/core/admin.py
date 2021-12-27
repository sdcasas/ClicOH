from django.contrib import admin

from core.models import Product, Order, OrderDetail


class OrderDetailStackInline(admin.TabularInline):
    model = OrderDetail
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("datetime_register", "_get_total", "_get_total_usd")
    inlines = (OrderDetailStackInline, )

    def _get_total(self, obj):
        return obj.get_total()

    def _get_total_usd(self, obj):
        return obj.get_total_usd()

    _get_total.short_description = "Total Factura"
    _get_total_usd.short_description = "Total Factura $USD"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock")