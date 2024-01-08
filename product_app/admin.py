from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Maxsulot, OrderItems, Order, CartItems
from .resources import MaxsulotResource, OrderResource, OrderItemsResource, CartItemsResource

class MaxsulotAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = MaxsulotResource

admin.site.register(Maxsulot, MaxsulotAdmin)

class OrderItemsAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrderItemsResource

admin.site.register(OrderItems, OrderItemsAdmin)

class OrderAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrderResource
    list_display = ['id', 'foydalanuvchi', 'jami_maxsulot', 'bekor_qilish_sababi', 'created_at', 'status']

admin.site.register(Order, OrderAdmin)

class CartItemsAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = CartItemsResource

admin.site.register(CartItems, CartItemsAdmin)