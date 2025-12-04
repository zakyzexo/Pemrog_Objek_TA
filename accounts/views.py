from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from orders.models import Order
from accounts.models import Profile, RestaurantProfile, DriverProfile
from .forms import RegisterForm
from .models import Profile, RestaurantProfile, CustomerProfile, DriverProfile


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data.get('role')
            Profile.objects.create(user=user, role=role)

            # Buat profil kosong sesuai role
            if role == 'restaurant':
                RestaurantProfile.objects.create(
                    user=user,
                    nama_restoran="",
                    alamat="",
                    deskripsi="",
                    jam_buka="00:00",
                    jam_tutup="00:00",
                    status_buka=False,
                    kategori=""
                )

            login(request, user)

            return redirect('after_login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def home(request):
    return render(request, 'accounts/home.html')


@login_required
def redirect_after_login(request):
    profile = Profile.objects.get(user=request.user)

    # kalau akun disuspend
    if profile.is_suspended:
        logout(request)
        return HttpResponse("Akun Anda sedang disuspend. Hubungi admin.")

    # kalau akun dihapus (soft delete)
    if profile.is_deleted:
        logout(request)
        return HttpResponse("Akun ini sudah dihapus oleh admin.")

    # normal redirect
    if profile.role == 'customer':
        return redirect('customer_dashboard')
    if profile.role == 'restaurant':
        return redirect('restaurant_dashboard')
    if profile.role == 'driver':
        return redirect('driver_dashboard')

    return redirect('admin_dashboard')




@login_required
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')


@login_required
def restaurant_dashboard(request):
    user = request.user

    try:
        resto = RestaurantProfile.objects.get(user=user)

        if not resto.nama_restoran or resto.nama_restoran.strip() == "":
            return redirect('lengkapi_profil_restoran')

    except RestaurantProfile.DoesNotExist:
        return redirect('lengkapi_profil_restoran')

    return render(request, 'accounts/restaurant_dashboard.html', {
        "resto": resto
    })



@login_required
def driver_dashboard(request):
    return render(request, 'accounts/driver_dashboard.html')


@login_required
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')


@login_required
def lengkapi_profil_restoran(request):
    user = request.user

    try:
        resto = RestaurantProfile.objects.get(user=user)
    except RestaurantProfile.DoesNotExist:
        resto = RestaurantProfile(user=user)

    if request.method == "POST":
        resto.nama_restoran = request.POST.get("nama_restoran")
        resto.alamat = request.POST.get("alamat")
        resto.deskripsi = request.POST.get("deskripsi")
        resto.jam_buka = request.POST.get("jam_buka")
        resto.jam_tutup = request.POST.get("jam_tutup")

        foto = request.FILES.get("foto_logo")
        if foto:
            resto.foto_logo = foto

        resto.save()
        return redirect("restaurant_dashboard")

    return render(request, "accounts/restaurant_profile_form.html", {"resto": resto})


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_rest = RestaurantProfile.objects.count()
    total_driver = DriverProfile.objects.count()
    total_orders = Order.objects.count()

    status_count = {
        "pending": Order.objects.filter(status="pending").count(),
        "processing": Order.objects.filter(status="processing").count(),
        "delivering": Order.objects.filter(status="delivering").count(),
        "finished": Order.objects.filter(status="finished").count(),
    }

    return render(request, "admin/dashboard.html", {
        "total_users": total_users,
        "total_rest": total_rest,
        "total_driver": total_driver,
        "total_orders": total_orders,
        "status_count": status_count,
    })

@login_required
def admin_users(request):
    users = Profile.objects.select_related("user")

    return render(request, "admin/users.html", {
        "users": users
    })


@login_required
def admin_restaurants(request):
    restaurants = RestaurantProfile.objects.all()
    return render(request, "admin/restaurants.html", {"restaurants": restaurants})


@login_required
def admin_drivers(request):
    drivers = DriverProfile.objects.all()
    return render(request, "admin/drivers.html", {"drivers": drivers})


@login_required
def admin_orders(request):
    orders = Order.objects.select_related("restaurant", "customer")
    return render(request, "admin/orders.html", {"orders": orders})


@login_required
def suspend_user(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    profile.is_suspended = True
    profile.save()
    messages.success(request, "User berhasil disuspend.")
    return redirect('admin_users')

@login_required
def unsuspend_user(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    profile.is_suspended = False
    profile.save()
    messages.success(request, "User berhasil diaktifkan kembali.")
    return redirect('admin_users')


@login_required
def delete_user(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    profile.is_deleted = True
    profile.save()
    messages.success(request, "User berhasil dihapus (soft delete).")
    return redirect('admin_users')


@login_required
def restore_user(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    profile.is_deleted = False
    profile.save()
    messages.success(request, "User berhasil dipulihkan.")
    return redirect('admin_users')