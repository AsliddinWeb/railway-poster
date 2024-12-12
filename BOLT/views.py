from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from product_app.models import Maxsulot, CartItems, Order, OrderItems, Kategoriya
from settings_app.models import SiteSettings, AdminParol
from user_app.models import User

@login_required(login_url='login_page')
def home_page(request):
    site_settings = SiteSettings.objects.last()
    today = timezone.now().date()
    
    if request.user.is_superuser:
        if request.user.username == "sklad":
            orders = Order.objects.filter(kimga="2")
            orders_1 = orders.filter(status='1')
            orders_2 = orders.filter(status='2')
            orders_3 = orders.filter(status='3')

            today_orders = orders.filter(created_at__date=today)
            today_orders_1 = today_orders.filter(status='1')
            today_orders_2 = today_orders.filter(status='2')

            users = User.objects.all()
        else:
            orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))
            orders_1 = orders.filter(status='1')
            orders_2 = orders.filter(status='2')
            orders_3 = orders.filter(status='3')

            today_orders = orders.filter(created_at__date=today)
            today_orders_1 = today_orders.filter(status='1')
            today_orders_2 = today_orders.filter(status='2')

            users = User.objects.all()

        admin_ctx = {
            'site_settings': site_settings,
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
        kategoriya = get_object_or_404(Kategoriya, id=1)
        maxsulotlar = Maxsulot.objects.filter(Q(kategoriya=kategoriya) | Q(kategoriya__isnull=True))
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = cart_items.count()
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1

        user_ctx = {
            'site_settings': site_settings,
            'maxsulotlar': maxsulotlar,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
        }

        return render(request, 'user-home.html', user_ctx)
    
    else:
        return redirect('login_page')

@login_required(login_url='login_page')
def user_sklad(request):
    if request.user.is_staff and request.user.username == "sklad":
        site_settings = SiteSettings.objects.last()
        kategoriya = get_object_or_404(Kategoriya, pk=2)
        maxsulotlar = Maxsulot.objects.filter(kategoriya=kategoriya)
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = cart_items.count()
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1

        user_ctx = {
            'site_settings': site_settings,
            'maxsulotlar': maxsulotlar,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
        }

        return render(request, 'user-sklad.html', user_ctx)
    
    else:
        return redirect('home_page')

@login_required(login_url='login_page')
def superadmin_product_page(request):
    if request.user.is_superuser:
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
        cart_item = CartItems.objects.filter(maxsulot=product, foydalanuvchi=request.user)

        if cart_item.exists():
            cart_item.delete()

        CartItems.objects.create(
            maxsulot=product,
            soni=int(request.POST.get('qty', 1)),
            foydalanuvchi=request.user
        )

        return redirect('home_page')

    return redirect('home_page')




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt  # Remove this in production and use proper CSRF handling
@login_required
def update_cart_quantity(request):
    if request.method == "POST":
        try:
            # Parse JSON body
            data = json.loads(request.body)
            cart_item_id = data.get("cart_item_id")
            new_quantity = data.get("new_quantity")

            if not cart_item_id or not new_quantity:
                return JsonResponse({"success": False, "message": "Invalid data"})

            cart_item = CartItems.objects.get(id=cart_item_id, foydalanuvchi=request.user)
            cart_item.soni = int(new_quantity)
            cart_item.save()

            return JsonResponse({"success": True, "message": "Quantity updated successfully"})
        except CartItems.DoesNotExist:
            return JsonResponse({"success": False, "message": "Cart item not found"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})

    return JsonResponse({"success": False, "message": "Invalid request"})




@login_required(login_url='login_page')
def remove_item_cart(request, item_id):
    cart_item = get_object_or_404(CartItems, id=item_id)
    if cart_item:
        cart_item.delete()
    return redirect('home_page')

@login_required(login_url='login_page')
def remove_all_cart(request):
    CartItems.objects.filter(foydalanuvchi=request.user).delete()
    return redirect('home_page')

@login_required(login_url='login_page')
def order_page(request):
    site_settings = SiteSettings.objects.last()
    maxsulotlar = Maxsulot.objects.all()
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
    cart_item_count = cart_items.count()
    order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1

    user_ctx = {
        'site_settings': site_settings,
        'maxsulotlar': maxsulotlar,
        'order_id': order_id,
        'cart_items': cart_items,
        'cart_item_count': cart_item_count,
    }

    if request.method == "POST":
        if cart_items.exists():
            order_instance = Order.objects.create(
                foydalanuvchi=request.user,
                jami_maxsulot=0,
                status='1',
                qoshimcha_rasm=request.FILES.get('qoshimchaRasm', None),
                qoshimcha_matn=request.POST.get('qoshimchaMatn', None),
                kimga=request.POST.get('kimga', None)
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
            
            order_instance.jami_maxsulot = k
            order_instance.save()
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
        site_settings = SiteSettings.objects.last()
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = cart_items.count()
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1
        user_orders = Order.objects.filter(foydalanuvchi=request.user)

        user_ctx = {
            'site_settings': site_settings,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
            'user_orders': user_orders,
            'user_orders_1': user_orders.filter(status='1'),
            'user_orders_2': user_orders.filter(status='2'),
            'user_orders_3': user_orders.filter(status='3'),
        }

        return render(request, 'user-profile.html', user_ctx)

@login_required(login_url='login_page')
def order_detail_page(request, pk):
    if request.user.is_superuser:
        return redirect('home_page')
    elif request.user.is_staff:
        order = get_object_or_404(Order, id=pk)
        site_settings = SiteSettings.objects.last()
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = cart_items.count()
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1

        user_ctx = {
            'site_settings': site_settings,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
            'order': order,
        }

        return render(request, 'order-detail.html', user_ctx)

@login_required(login_url='login_page')
def superadmin_all_orders_page(request):
    if request.user.is_superuser:
        site_settings = SiteSettings.objects.last()

        if request.user.username == "sklad":
            all_orders = Order.objects.filter(kimga="2")
        else:
            all_orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))
        orders = all_orders.filter(status='1')  # Only orders with status '1'
        orders_1_count = all_orders.filter(status='1').count()
        orders_2_count = all_orders.filter(status='2').count()
        orders_3_count = all_orders.filter(status='3').count()
        admin_ctx = {
            'site_settings': site_settings,
            'orders': orders,
            'orders_1': orders_1_count,
            'orders_2': orders_2_count,
            'orders_3': orders_3_count,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    
    else:
        return redirect('home_page')



@login_required(login_url='login_page')
def superadmin_orders_1_page(request):
    if request.user.is_superuser:
        site_settings = SiteSettings.objects.last()

        # Retrieve all relevant orders based on `kimga` and `username`
        if request.user.username == "sklad":
            all_orders = Order.objects.filter(kimga="2")
        else:
            all_orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))

        # Filter for each status
        orders = all_orders.filter(status='1')  # Only orders with status '1'
        orders_1_count = all_orders.filter(status='1').count()
        orders_2_count = all_orders.filter(status='2').count()
        orders_3_count = all_orders.filter(status='3').count()

        admin_ctx = {
            'site_settings': site_settings,
            'orders': orders,
            'orders_1': orders_1_count,
            'orders_2': orders_2_count,
            'orders_3': orders_3_count,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    else:
        return redirect('home_page')





@login_required(login_url='login_page')
def superadmin_orders_2_page(request):
    if request.user.is_superuser:
        site_settings = SiteSettings.objects.last()

        # Retrieve all relevant orders based on `kimga` and `username`
        if request.user.username == "sklad":
            all_orders = Order.objects.filter(kimga="2")
        else:
            all_orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))

        # Filter for each status
        orders = all_orders.filter(status='2')  # Only orders with status '2'
        orders_1_count = all_orders.filter(status='1').count()
        orders_2_count = all_orders.filter(status='2').count()
        orders_3_count = all_orders.filter(status='3').count()

        admin_ctx = {
            'site_settings': site_settings,
            'orders': orders,
            'orders_1': orders_1_count,
            'orders_2': orders_2_count,
            'orders_3': orders_3_count,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    else:
        return redirect('home_page')



@login_required(login_url='login_page')
def superadmin_orders_3_page(request):
    if request.user.is_superuser:
        site_settings = SiteSettings.objects.last()

        # Retrieve all relevant orders based on `kimga` and `username`
        if request.user.username == "sklad":
            all_orders = Order.objects.filter(kimga="2")
        else:
            all_orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))

        # Filter for each status
        orders = all_orders.filter(status='3')  # Only orders with status '3'
        orders_1_count = all_orders.filter(status='1').count()
        orders_2_count = all_orders.filter(status='2').count()
        orders_3_count = all_orders.filter(status='3').count()

        admin_ctx = {
            'site_settings': site_settings,
            'orders': orders,
            'orders_1': orders_1_count,
            'orders_2': orders_2_count,
            'orders_3': orders_3_count,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    else:
        return redirect('home_page')
@login_required(login_url='login_page')
def superadmin_edit_order_page(request, pk):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=pk)

        if request.method == "POST":
            if 'sabab' in request.POST:
                order.status = '3'
                order.bekor_qilish_sababi = request.POST.get('sabab')
                order.save()
            elif 'parol' in request.POST:
                parol_input = request.POST.get('parol')
                parol = AdminParol.objects.last()
                if parol and int(parol_input) == int(parol.parol):
                    order.status = '2'
                    order.save()

        site_settings = SiteSettings.objects.last()
        orders_1_count = Order.objects.filter(status='1').count()
        orders_2_count = Order.objects.filter(status='2').count()
        orders_3_count = Order.objects.filter(status='3').count()
        print(f"Counts : {orders_1_count}, {orders_2_count}, {orders_3_count}")

        admin_ctx = {
            'site_settings': site_settings,
            'order': order,
            "orders_1": orders_1_count,
            "orders_2": orders_2_count,
            "orders_3": orders_3_count
        }

        return render(request, 'admin-order-edit.html', admin_ctx)
    
    else:
        return redirect('home_page')

@login_required(login_url='login_page')
def superadmin_order_status_2(request, pk):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=pk)
        order.status = '2'
        order.save()
        return redirect('superadmin_edit_order_page', pk=pk)
    else:
        return redirect('home_page')
