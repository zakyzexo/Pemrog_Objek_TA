from django.contrib.auth import views as auth_views
from django.urls import path
from .views import register, customer_dashboard, restaurant_dashboard, driver_dashboard, admin_dashboard, redirect_after_login, logout_user, lengkapi_profil_restoran, admin_users, admin_restaurants, admin_drivers, admin_orders, suspend_user, unsuspend_user, delete_user, restore_user

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
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/users/', admin_users, name='admin_users'),
    path('admin/restaurants/', admin_restaurants, name='admin_restaurants'),
    path('admin/drivers/', admin_drivers, name='admin_drivers'),
    path('admin/orders/', admin_orders, name='admin_orders'),
    path('admin/user/suspend/<int:user_id>/', suspend_user, name='suspend_user'),
    path('admin/user/unsuspend/<int:user_id>/', unsuspend_user, name='unsuspend_user'),
    path('admin/user/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('admin/user/restore/<int:user_id>/', restore_user, name='restore_user'),

]
