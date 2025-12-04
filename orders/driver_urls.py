from django.urls import path
from .views_driver import driver_dashboard, ready_orders, take_order, my_orders, finish_order

urlpatterns = [
    path('dashboard/', driver_dashboard, name='driver_dashboard'),
    path('ready/', ready_orders, name='driver_ready_orders'),
    path('take/<int:order_id>/', take_order, name='driver_take_order'),
    path('my-orders/', my_orders, name='driver_my_orders'),
    path('finish/<int:order_id>/', finish_order, name='driver_finish_order'),
]
