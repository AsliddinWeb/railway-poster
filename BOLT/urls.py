from django.contrib import admin
from django.urls import path, include

# Static settings
from django.conf import settings
from django.conf.urls.static import static

from .views import home_page, \
    add_to_cart, remove_item_cart, remove_all_cart, order_page, profile_page, \
    order_detail_page, superadmin_all_orders_page, \
    superadmin_orders_1_page, superadmin_orders_2_page, superadmin_orders_3_page, \
    superadmin_edit_order_page, superadmin_order_status_2

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('auth/', include('user_app.urls')),

    # Ui routes
    path('', home_page, name='home_page'),

    # User
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-item-cart/<int:item_id>/', remove_item_cart, name='remove_item_cart'),

    path('remove-all-cart/', remove_all_cart, name='remove_all_cart'),
    path('order/', order_page, name='order_page'),

    path('kabinet/', profile_page, name='profile_page'),
    path('kabinet/order/<int:pk>/', order_detail_page, name='order_detail_page'),

    # Admin
    path('all-orders/', superadmin_all_orders_page, name='superadmin_all_orders_page'),
    path('buyurtma-berilganlar/', superadmin_orders_1_page, name='superadmin_orders_1_page'),
    path('yetkazib-berilganlar/', superadmin_orders_2_page, name='superadmin_orders_2_page'),
    path('bekor-qilinganlar/', superadmin_orders_3_page, name='superadmin_orders_3_page'),

    path('edit-order/<int:pk>/', superadmin_edit_order_page, name='superadmin_edit_order_page'),
    path('edit-order/success/<int:pk>/', superadmin_order_status_2, name='superadmin_order_status_2'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)