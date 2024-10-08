from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from product_app.models import Maxsulot, CartItems, Order, OrderItems
from settings_app.models import SiteSettings

from django.utils import timezone
from user_app.models import User

@login_required(login_url='login_page')
def home_page(request):
    if request.user.is_superuser:
        # Required
        site_settings = SiteSettings.objects.last()

        # Main
        orders = Order.objects.all()

        orders_1 = Order.objects.filter(status='1')
        orders_2 = Order.objects.filter(status='2')
        orders_3 = Order.objects.filter(status='3')

        today = timezone.now().date()
        today_orders = Order.objects.filter(created_at__date=today)

        today_orders_1 = Order.objects.filter(created_at__date=today, status='1')
        today_orders_2 = Order.objects.filter(created_at__date=today, status='2')

        users = User.objects.all()

        # CTX
        admin_ctx = {
            # Required
            'site_settings': site_settings,

            # Main
            'orders': orders,
            'top_orders': orders[:10],
            'orders_1': orders_1,
            'orders_2': orders_2,
            'orders_3': orders_3,

            'today_orders': today_orders,

            'today_orders_1': today_orders_1,
            'today_orders_2': today_orders_2,
            'users': users,
        }

        return render(request, 'admin-home.html', admin_ctx)
    elif request.user.is_staff:
        # Requirements
        site_settings = SiteSettings.objects.last()
        maxsulotlar = Maxsulot.objects.all()

        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = len(cart_items)

        if Order.objects.first():
            order_id = int(Order.objects.first().id) + 1
        else:
            order_id = 1

        user_ctx = {
            'site_settings': site_settings,
            'maxsulotlar': maxsulotlar,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
        }
        return render(request, 'user-home.html', user_ctx)

@login_required(login_url='login_page')
def superadmin_product_page(request):
    if request.user.is_superuser:
        # Requirements
        maxsulotlar = Maxsulot.objects.all()

        user_ctx = {
            'maxsulotlar': maxsulotlar,
        }
        return render(request, 'user-home.html', user_ctx)
    else:
        return redirect('home_page')

@login_required(login_url='login_page')
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Maxsulot, id=product_id)

        # Add to cart
        cart_item = CartItems.objects.filter(maxsulot=product, foydalanuvchi=request.user)
        if len(cart_item) > 0:
            cart_item.delete()
            CartItems.objects.create(
                maxsulot=product,
                soni=int(request.POST.get('qty', 1)),
                foydalanuvchi=request.user
            )
            return redirect('home_page')
        else:
            CartItems.objects.create(
                maxsulot=product,
                soni=int(request.POST.get('qty', 1)),
                foydalanuvchi=request.user
            )
            return redirect('home_page')
    return redirect('home_page')

@login_required(login_url='login_page')
def remove_item_cart(request, item_id):
    cart_item = get_object_or_404(CartItems, id=item_id)
    print(cart_item)
    if cart_item:
        cart_item.delete()
        return redirect('home_page')
    return redirect('home_page')

@login_required(login_url='login_page')
def remove_all_cart(request):
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
    for i in cart_items:
        i.delete()
    return redirect('home_page')

@login_required(login_url='login_page')
def order_page(request):
    # Requirements
    site_settings = SiteSettings.objects.last()
    maxsulotlar = Maxsulot.objects.all()

    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
    cart_item_count = 0

    if Order.objects.first():
        order_id = int(Order.objects.first().id) + 1
    else:
        order_id = 1

    user_ctx = {
        'site_settings': site_settings,
        'maxsulotlar': maxsulotlar,
        'order_id': order_id,
        'cart_items': cart_items,
        'cart_item_count': cart_item_count,
    }

    if request.method == "POST":
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)

        if cart_items:
            order_instance = Order.objects.create(
                foydalanuvchi=request.user,
                jami_maxsulot=0,
                status='1',
                qoshimcha_rasm=request.FILES.get('qoshimchaRasm', None),
                qoshimcha_matn=request.POST.get('qoshimchaMatn', None),
            )
            k = 0
            for item in cart_items:
                maxsulot = OrderItems.objects.create(
                    maxsulot=item.maxsulot,
                    soni=item.soni,
                    foydalanuvchi=item.foydalanuvchi,
                )
                item.delete()
                k += maxsulot.soni
                order_instance.maxsulotlar.add(maxsulot)
            print(k)
            order_instance.jami_maxsulot = k
            order_instance.save()

            # Order ctx
            user_ctx['order'] = order_instance
        else:
            return redirect('home_page')

        return render(request, 'order-success.html', user_ctx)
    return render(request, 'order-success.html', user_ctx)

@login_required(login_url='login_page')
def profile_page(request):
    if request.user.is_superuser:
        return redirect('home_page')
    elif request.user.is_staff:
        # Requirements
        site_settings = SiteSettings.objects.last()

        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = len(cart_items)

        if Order.objects.first():
            order_id = int(Order.objects.first().id) + 1
        else:
            order_id = 1

        # Main
        user_orders = Order.objects.filter(foydalanuvchi=request.user)

        user_orders_1 = Order.objects.filter(foydalanuvchi=request.user, status='1')
        user_orders_2 = Order.objects.filter(foydalanuvchi=request.user, status='2')
        user_orders_3 = Order.objects.filter(foydalanuvchi=request.user, status='3')

        user_ctx = {
            'site_settings': site_settings,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
            'user_orders': user_orders,

            'user_orders_1': user_orders_1,
            'user_orders_2': user_orders_2,
            'user_orders_3': user_orders_3,
        }
        return render(request, 'user-profile.html', user_ctx)


@login_required(login_url='login_page')
def order_detail_page(request, pk):
    if request.user.is_superuser:
        return redirect('home_page')
    elif request.user.is_staff:
        order = get_object_or_404(Order, id=pk)
        # Requirements
        site_settings = SiteSettings.objects.last()

        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = len(cart_items)

        if Order.objects.first():
            order_id = int(Order.objects.first().id) + 1
        else:
            order_id = 1

        # Main


        user_ctx = {
            'site_settings': site_settings,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,

            # Main
            'order': order,
        }
        return render(request, 'order-detail.html', user_ctx)

@login_required(login_url='login_page')
def superadmin_all_orders_page(request):
    if request.user.is_superuser:
        # Required
        site_settings = SiteSettings.objects.last()

        # Main
        orders = Order.objects.all()

        # CTX
        admin_ctx = {
            # Required
            'site_settings': site_settings,

            # Main
            'orders': orders,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    else:
        redirect('home_page')

@login_required(login_url='login_page')
def superadmin_orders_1_page(request):
    if request.user.is_superuser:
        # Required
        site_settings = SiteSettings.objects.last()

        # Main
        orders = Order.objects.filter(status='1')

        # CTX
        admin_ctx = {
            # Required
            'site_settings': site_settings,

            # Main
            'orders': orders,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    else:
        redirect('home_page')

@login_required(login_url='login_page')
def superadmin_orders_2_page(request):
    if request.user.is_superuser:
        # Required
        site_settings = SiteSettings.objects.last()

        # Main
        orders = Order.objects.filter(status='2')

        # CTX
        admin_ctx = {
            # Required
            'site_settings': site_settings,

            # Main
            'orders': orders,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    else:
        redirect('home_page')

@login_required(login_url='login_page')
def superadmin_orders_3_page(request):
    if request.user.is_superuser:
        # Required
        site_settings = SiteSettings.objects.last()

        # Main
        orders = Order.objects.filter(status='3')

        # CTX
        admin_ctx = {
            # Required
            'site_settings': site_settings,

            # Main
            'orders': orders,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    else:
        redirect('home_page')

@login_required(login_url='login_page')
def superadmin_edit_order_page(request, pk):
    if request.user.is_superuser:
        # Main
        order = get_object_or_404(Order, id=pk)
        if request.method == "POST":
            order.status = '3'
            order.bekor_qilish_sababi = request.POST.get('sabab', None)
            order.save()
            
        # Required
        site_settings = SiteSettings.objects.last()



        # CTX
        admin_ctx = {
            # Required
            'site_settings': site_settings,

            # Main
            'order': order,
        }

        return render(request, 'admin-order-edit.html', admin_ctx)
    else:
        redirect('home_page')

@login_required(login_url='login_page')
def superadmin_order_status_2(request, pk):
    if request.user.is_superuser:
        # Main
        order = get_object_or_404(Order, id=pk)
        if order:
            order.status = '2'
            order.save()
            return redirect('superadmin_edit_order_page', pk=pk)
