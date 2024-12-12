from django.contrib import admin
from django.http import HttpResponse
from import_export.admin import ImportExportMixin
import os

from BOLT.settings import BASE_DIR
from .models import Maxsulot, OrderItems, Order, CartItems, Kategoriya
from .resources import MaxsulotResource, OrderResource, OrderItemsResource, CartItemsResource


class MaxsulotAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = MaxsulotResource


admin.site.register(Kategoriya)
admin.site.register(Maxsulot, MaxsulotAdmin)


class OrderItemsAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrderItemsResource


admin.site.register(OrderItems, OrderItemsAdmin)





class OrderAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrderResource

    def export_orders_with_template(self, request, queryset):
        """
        Export orders using an XLSX template.
        """
        # Resolve the path to the template
        template_path = os.path.join(BASE_DIR, "static", "succes_orders.xlsx")
        if not os.path.exists(template_path):
            self.message_user(request, f"Shablon topilmadi {template_path}", level='error')
            return

        queryset = queryset.filter(status='2')  # Example filter for status '2'

        resource = self.resource_class()
        xlsx_content = resource.export_to_template_xlsx(queryset, template_path)

        response = HttpResponse(
            xlsx_content,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response['Content-Disposition'] = 'attachment; filename="succes_orders.xlsx"'
        return response

    export_orders_with_template.short_description = "Yetkazib berilgan mahsulotlarni yuklash"
    actions = ['export_orders_with_template']

admin.site.register(Order, OrderAdmin)




















class CartItemsAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = CartItemsResource


admin.site.register(CartItems, CartItemsAdmin)
