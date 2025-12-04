from django.contrib.auth import views as auth_views
from django.urls import path
from .views import register, customer_dashboard, restaurant_dashboard, driver_dashboard, admin_dashboard, redirect_after_login, logout_user, lengkapi_profil_restoran

urlpatterns = [
    path('register/', register, name='register'),
    path('customer/dashboard/', customer_dashboard, name='customer_dashboard'),
    path('restaurant/dashboard/', restaurant_dashboard, name='restaurant_dashboard'),
    path('driver/dashboard/', driver_dashboard, name='driver_dashboard'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True, success_url='/accounts/after-login/'), name='login'),
    path('logout/', logout_user, name='logout'),
    path('after-login/', redirect_after_login, name='after_login'),
    path('restaurant/lengkapi-profil/', lengkapi_profil_restoran, name='lengkapi_profil_restoran'),

]
