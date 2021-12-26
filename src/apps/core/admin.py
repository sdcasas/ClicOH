from django.contrib import admin

from core.models import Product, Order, OrderDetail


class OrderDetailStackInline(admin.TabularInline):
    model = OrderDetail
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderDetailStackInline, )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock")