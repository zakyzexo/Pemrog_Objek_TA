from django.urls import path
from .views import tambah_menu, daftar_menu, edit_menu, delete_menu, add_to_cart, lihat_cart
from . import views

urlpatterns = [
    path('tambah-menu/', views.tambah_menu, name='tambah_menu'),
    path('menu/', views.daftar_menu, name='daftar_menu'),
    path('menu/edit/<int:menu_id>/', views.edit_menu, name='edit_menu'),
    path('menu/delete/<int:menu_id>/', views.delete_menu, name='delete_menu'),
    path('cart/add/<int:menu_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', lihat_cart, name='lihat_cart'),
    path('orders/', views.daftar_order, name='daftar_order'),
    path('orders/<int:order_id>/', views.detail_order, name='detail_order'),
]
