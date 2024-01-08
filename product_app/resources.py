from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Maxsulot, OrderItems, Order, CartItems
from user_app.models import User

class MaxsulotResource(resources.ModelResource):
    class Meta:
        model = Maxsulot
        fields = ('nomi', 'rasm', 'foydalanuvchi__username', 'razmer', 'qoshimcha')

class OrderItemsResource(resources.ModelResource):
    maxsulot = fields.Field(
        column_name='maxsulot',
        attribute='maxsulot',
        widget=ForeignKeyWidget(Maxsulot, 'nomi')
    )

    class Meta:
        model = OrderItems
        fields = ('maxsulot', 'soni', 'foydalanuvchi__username')

class CartItemsResource(resources.ModelResource):
    maxsulot = fields.Field(
        column_name='maxsulot',
        attribute='maxsulot',
        widget=ForeignKeyWidget(Maxsulot, 'nomi')
    )

    class Meta:
        model = CartItems
        fields = ('maxsulot', 'soni', 'foydalanuvchi__username')

class OrderResource(resources.ModelResource):
    maxsulotlar = fields.Field(
        column_name='maxsulotlar',
        attribute='maxsulotlar',
        widget=ForeignKeyWidget(OrderItems, 'id')
    )

    class Meta:
        model = Order
        fields = ('maxsulotlar__maxsulot__nomi', 'foydalanuvchi__username', 'jami_maxsulot', 'status', 'bekor_qilish_sababi', 'qoshimcha_rasm', 'qoshimcha_matn', 'created_at', 'updated_at')
