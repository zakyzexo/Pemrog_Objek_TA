from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem
from restaurant.models import Cart, CartItem
from accounts.models import RestaurantProfile
from orders.models import Order, ChatMessage
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



@login_required
def customer_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-tanggal_order')
    return render(request, "orders/customer_orders.html", {
        "orders": orders
    })


@login_required
def checkout(request):
    user = request.user

    # Ambil cart user
    try:
        cart = Cart.objects.get(customer=user)
    except Cart.DoesNotExist:
        return redirect("lihat_cart")   # kalau cart kosong

    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect("lihat_cart")

    # ====== POST: buat order ======
    if request.method == "POST":

        # Tentukan restoran (semua item pasti dari 1 restoran)
        restoran = cart_items.first().menu.restaurant

        # Hitung total
        total = sum(item.subtotal for item in cart_items)

        # Buat order
        order = Order.objects.create(
            customer=user,
            restaurant=restoran,
            total_harga=total,
            status="diterima"
        )

        # Pindahkan cart item → order item
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menu=item.menu,
                qty=item.qty,
                subtotal=item.subtotal
            )

        # Kosongkan cart
        cart_items.delete()

        return redirect("customer_orders")

    # ========= GET: tampilkan ringkasan checkout =========
    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total": sum(item.subtotal for item in cart_items)
    })


def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return render(request, "orders/checkout_empty.html")

    items = []
    total = 0

    for menu_id, qty in cart.items():
        menu = Menu.objects.get(id=menu_id)
        subtotal = menu.harga * qty
        items.append({
            "menu": menu,
            "qty": qty,
            "subtotal": subtotal
        })
        total += subtotal

    return render(request, "orders/checkout.html", {
        "items": items,
        "total": total
    })


def process_checkout(request):
    if request.method != "POST":
        return redirect("checkout")

    cart = request.session.get("cart", {})
    if not cart:
        return redirect("checkout")

    customer = request.user
    customer_profile = CustomerProfile.objects.get(user=customer)

    # 1. Buat Order
    order = Order.objects.create(
        customer=customer_profile,
        status="pending",
        total_price=0
    )

    total = 0

    # 2. Masukkan semua item cart ke OrderItem
    for menu_id, qty in cart.items():
        menu = Menu.objects.get(id=menu_id)
        subtotal = menu.harga * qty
        total += subtotal

        OrderItem.objects.create(
            order=order,
            menu=menu,
            quantity=qty,
            price=menu.harga
        )

    # 3. Update total
    order.total_price = total
    order.save()

    # 4. Kosongkan keranjang
    request.session["cart"] = {}

    return render(request, "orders/checkout_success.html", {
        "order": order
    })


def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
        return redirect("restaurant_orders")  # halaman daftar order restoran

    return render(request, "orders/update_status.html", {
        "order": order,
    })


def restaurant_orders(request):
    resto = RestaurantProfile.objects.get(user=request.user)
    orders = Order.objects.filter(restaurant=resto).order_by("-created_at")

    return render(request, "orders/restaurant_orders.html", {
        "orders": orders
    })


@login_required
def customer_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    items = OrderItem.objects.filter(order=order)

    return render(request, "orders/customer_order_detail.html", {
        "order": order,
        "items": items
    })


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if order.status != "pending":
        messages.error(request, "Pesanan tidak bisa dibatalkan karena sedang diproses.")
        return redirect("customer_order_detail", order_id=order.id)

    order.status = "cancelled"
    order.save()

    messages.success(request, "Pesanan berhasil dibatalkan.")
    return redirect("customer_orders")

@login_required
def chat_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # pastikan hanya customer PEMILIK order atau driver YANG MENGAMBIL order yang bisa akses
    # (sesuaikan dengan modelmu)
    if request.user != order.customer and request.user != getattr(order, "driver", None):
        return redirect("customer_dashboard")

    # kalau POST → simpan pesan baru
    if request.method == "POST":
        isi = request.POST.get("isi_pesan")
        if isi and isi.strip():
            ChatMessage.objects.create(
                order=order,
                pengirim=request.user,
                isi_pesan=isi
            )
        return redirect("chat_order", order_id=order.id)

    # semua chat untuk order tersebut
    pesan_list = ChatMessage.objects.filter(order=order).order_by("waktu")

    return render(request, "orders/chat_room.html", {
        "order": order,
        "pesan_list": pesan_list
    })


@login_required
def get_chat_messages(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Hanya customer / resto / driver yg terkait boleh baca
    if request.user not in [order.customer, order.restaurant.user, order.driver.user if order.driver else None]:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    messages = OrderChat.objects.filter(order=order)

    data = []
    for m in messages:
        data.append({
            "sender": m.sender.profile.role,  # customer/restaurant/driver
            "message": m.message,
            "timestamp": m.timestamp.strftime("%H:%M"),
            "is_me": (m.sender == request.user)
        })

    return JsonResponse({"messages": data})

@login_required
def send_chat_message(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        msg = request.POST.get("message")

        if msg.strip() != "":
            OrderChat.objects.create(
                order=order,
                sender=request.user,  # <-- penting
                message=msg
            )

    return redirect('chat_order', order_id=order_id)
