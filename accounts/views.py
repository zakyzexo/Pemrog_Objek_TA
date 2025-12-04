from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from .models import Profile, RestaurantProfile
from django.contrib.auth.decorators import login_required
from accounts.models import CustomerProfile, RestaurantProfile, DriverProfile
from django.contrib.auth import logout
# from restaurant.models import RestaurantProfile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Simpan user
            user = form.save()

            # Buat profile untuk user tersebut
            role = form.cleaned_data.get('role')
            Profile.objects.create(user=user, role=role)

            # Jika role = restaurant, buat RestaurantProfile kosong
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

            # Login otomatis setelah register (opsional)
            login(request, user)

            # Redirect berdasar role
            if role == 'customer':
                return redirect('customer_dashboard')
            elif role == 'restaurant':
                return redirect('restaurant_dashboard')
            elif role == 'driver':
                return redirect('driver_dashboard')
            else:
                return redirect('admin_dashboard')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def home(request):
    return render(request, 'accounts/home.html')


@login_required
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')

@login_required
def restaurant_dashboard(request):
    return render(request, 'accounts/restaurant_dashboard.html')

@login_required
def driver_dashboard(request):
    return render(request, 'accounts/driver_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

@login_required
def redirect_after_login(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    role = profile.role

    # -------------------------
    # ROLE CUSTOMER
    # -------------------------
    if role == 'customer':
        return redirect('customer_dashboard')

    # -------------------------
    # ROLE RESTAURANT
    # -------------------------
    if role == 'restaurant':
        try:
            resto = RestaurantProfile.objects.get(user=user)

            # Jika nama_restoran masih kosong → berarti profil belum lengkap
            if not resto.nama_restoran:
                return redirect('lengkapi_profil_restoran')
        except RestaurantProfile.DoesNotExist:
            return redirect('lengkapi_profil_restoran')

        return redirect('restaurant_dashboard')

    # -------------------------
    # ROLE DRIVER
    # -------------------------
    if role == 'driver':
        return redirect('driver_dashboard')

    if user.is_superuser:
        return redirect('admin_dashboard')

    return redirect('customer_dashboard')



@login_required
def lengkapi_profil_restoran(request):
    user = request.user
    
    # cek apakah profile sudah ada
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

    return render(request, "accounts/restaurant_profile_form.html", {
        "resto": resto
    })


# def customer_dashboard(request):
#     return render(request, 'accounts/customer_dashboard.html')

# def restaurant_dashboard(request):
#     return render(request, 'accounts/restaurant_dashboard.html')

# def driver_dashboard(request):
#     return render(request, 'accounts/driver_dashboard.html')

# def admin_dashboard(request):
#     return render(request, 'accounts/admin_dashboard.html')



def logout_user(request):
    logout(request)
    return redirect('login')