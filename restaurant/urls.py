from django.urls import path
from .views import tambah_menu, daftar_menu, edit_menu, delete_menu, add_to_cart, lihat_cart, restaurant_orders, order_detail, customer_list_restaurant, customer_lihat_menu, delete_cart_item, update_order_status, view_cart, checkout, checkout_page, buat_order
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
    path('orders/', restaurant_orders, name='restaurant_orders'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('restoran/', customer_list_restaurant, name='customer_restoran_list'),
    # customer lihat menu restoran
    path('<int:resto_id>/menu/', customer_lihat_menu, name='customer_lihat_menu'),
    path('cart/add/<int:menu_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/delete/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('cart/checkout/', checkout, name='checkout'),
    path('orders/update-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('cart/checkout/', checkout_page, name='checkout_page'),
    path('cart/buat-order/', buat_order, name='buat_order'),

]
