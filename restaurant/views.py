from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile, RestaurantProfile
from .forms import MenuForm
from restaurant.models import Menu
from django.shortcuts import get_object_or_404, redirect
from .models import Cart, CartItem
from .models import Menu
from accounts.models import RestaurantProfile
from django.contrib import messages
from orders.models import Order, OrderItem


@login_required
def tambah_menu(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    # hanya restoran boleh akses
    if profile.role != 'restaurant':
        return redirect('home')

    resto = RestaurantProfile.objects.get(user=user)

    if request.method == "POST":
        print("DEBUG nama_makanan =", request.POST.get('nama_makanan'))
        print("DEBUG POST =", request.POST)
        nama = request.POST.get('nama_makanan')
        deskripsi = request.POST.get('deskripsi')
        harga = request.POST.get('harga')
        status = request.POST.get('status')
        foto = request.FILES.get('foto_makanan')

        Menu.objects.create(
            restaurant=resto,
            nama_makanan=nama,
            deskripsi=deskripsi,
            harga=harga,
            status=status,
            foto_makanan=foto
        )

        return redirect('daftar_menu')

    print("TEMPLATE DIPAKAI:", 'restaurant/tambah_menu.html')
    return render(request, 'restaurant/tambah_menu.html', {'template_version': 'restaurant_v1'})
    
    messages.success(request, "Menu berhasil ditambahkan!")
    return redirect('daftar_menu')



@login_required
def daftar_menu(request):
    user = request.user

    # ambil role user
    profile = Profile.objects.get(user=user)
    if profile.role != 'restaurant':
        return redirect('home')

    # ambil profil restoran
    resto = RestaurantProfile.objects.get(user=request.user)

    # ambil menu milik restoran ini saja
    menu_list = Menu.objects.filter(restaurant=resto)

    return render(request, 'restaurant/daftar_menu.html', {'menu_list': menu_list})


@login_required
def edit_menu(request, id):
    user = request.user

    # cek role
    profile = Profile.objects.get(user=user)
    if profile.role != 'restaurant':
        return redirect('home')

    # ambil restoran
    resto = RestaurantProfile.objects.get(user=user)

    # ambil menu milik restoran ini saja (supaya tidak bisa edit menu orang lain)
    menu = get_object_or_404(Menu, id=id, restaurant=resto, restaurant_user=user)

    if request.method == 'POST':
        menu.nama_makanan = request.POST.get('nama_makanan')
        menu.harga = request.POST.get('harga')
        menu.deskripsi = request.POST.get('deskripsi')
        menu.status = request.POST.get('status')

        if 'foto_makanan' in request.FILES:
            menu.foto_makanan = request.FILES['foto_makanan']

        menu.save()
        return redirect('daftar_menu')

    return render(request, 'restaurant/edit_menu.html', {'form': form, 'menu': menu})

    messages.success(request, "Menu berhasil diperbarui!")
    return redirect('daftar_menu')


@login_required
def delete_menu(request, id):
    user = request.user

    # cek role
    profile = Profile.objects.get(user=user)
    if profile.role != 'restaurant':
        return redirect('home')

    # ambil restoran
    resto = RestaurantProfile.objects.get(user=user)

    # ambil menu hanya milik restoran ini
    menu = get_object_or_404(Menu, id=id, restaurant=resto, restaurant__user=user)

    if request.method == 'POST':
        menu.delete()
        return redirect('daftar_menu')

    # konfirmasi dulu
    return render(request, 'restaurant/delete_menu.html', {'menu': menu})

    messages.success(request, "Menu berhasil dihapus!")
    return redirect('daftar_menu')



@login_required
def add_to_cart(request, menu_id):
    user = request.user

    # Ambil menu
    menu = get_object_or_404(Menu, id=menu_id)

    # Cek apakah customer sudah punya cart
    cart, created = Cart.objects.get_or_create(customer=user)


     # Cek apakah cart berisi item dari restoran lain
    items = cart.items.all()

    if items.exists():
        current_restaurant = items.first().menu.restaurant
        if current_restaurant != menu.restaurant:
            # Kosongkan cart jika beda restoran
            items.delete()


    # Cek apakah item menu sudah ada di cart
    item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        menu=menu,
        defaults={'qty': 1, 'subtotal': menu.harga}
    )

    # Jika item sudah ada → tambah qty
    if not item_created:
        item.qty += 1
        item.subtotal = item.qty * menu.harga
        item.save()

    return redirect('lihat_cart')


@login_required
def lihat_cart(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    items = cart.items.all()
    total = sum(item.subtotal for item in items)

    return render(request, 'restaurant/cart.html', {
        'items': items,
        'total': total,
    })


@login_required
def daftar_order(request):
    restaurant_profile = RestaurantProfile.objects.get(user=request.user)

    orders = Order.objects.filter(
        restaurant=restaurant_profile
    ).order_by('-created_at')

    return render(request, 'restaurant/daftar_order.html', {
        'orders': orders
    })


@login_required
def detail_order(request, order_id):
    restaurant_profile = RestaurantProfile.objects.get(user=request.user)

    order = get_object_or_404(Order, id=order_id, restaurant=restaurant_profile)
    items = order.items.all()

    if request.method == "POST":
        status_baru = request.POST.get("status")
        order.status = status_baru
        order.save()
        messages.success(request, "Status pesanan berhasil diperbarui.")
        return redirect('detail_order', order_id=order.id)

    return render(request, 'restaurant/detail_order.html', {
        'order': order,
        'items': items
    })


@login_required
def restaurant_dashboard(request):
    user = request.user
    resto = RestaurantProfile.objects.get(user=user)

    # Hitung total menu
    total_menu = Menu.objects.filter(restaurant=resto).count()

    # Pesanan berdasarkan status
    total_masuk = Order.objects.filter(restaurant=resto, status__in=[
        'diterima', 'diproses', 'menunggu_driver'
    ]).count()

    total_selesai = Order.objects.filter(restaurant=resto, status='selesai').count()
    total_batal = Order.objects.filter(restaurant=resto, status='dibatalkan').count()

    # Ambil 5 pesanan terbaru
    pesanan_terbaru = Order.objects.filter(restaurant=resto).order_by('-created_at')[:5]

    return render(request, 'accounts/restaurant_dashboard.html', {
        'resto': resto,
        'total_menu': total_menu,
        'total_masuk': total_masuk,
        'total_selesai': total_selesai,
        'total_batal': total_batal,
        'pesanan_terbaru': pesanan_terbaru,
    })

