from django.contrib import admin

from .models import Maxsulot, OrderItems, Order, CartItems

admin.site.register(Maxsulot)

admin.site.register(OrderItems)

class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('maxsulotlar', )
admin.site.register(Order, OrderAdmin)

admin.site.register(CartItems)