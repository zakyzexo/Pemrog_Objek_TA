from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from functools import wraps
from accounts.decorators import role_required

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            try:
                profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                return redirect("home")

            # Jika role tidak sesuai, redirect ke home
            if profile.role != required_role:
                return redirect("home")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@role_required("customer")
def customer_dashboard(request):
    return render(request, "accounts/customer_dashboard.html")

@role_required("restaurant")
def restaurant_dashboard(request):
    return render(request, "accounts/restaurant_dashboard.html")

@role_required("driver")
def driver_dashboard(request):
    return render(request, "accounts/driver_dashboard.html")

@role_required("admin")
def admin_dashboard(request):
    return render(request, "accounts/admin_dashboard.html")
