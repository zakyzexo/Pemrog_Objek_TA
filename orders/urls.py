from django.urls import path
from .views import customer_orders, checkout, process_checkout, update_order_status, customer_order_detail, cancel_order, chat_order

urlpatterns = [
    path('customer/', customer_orders, name='customer_orders'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/process/', process_checkout, name='process_checkout'),
    path('restaurant/update-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('detail/<int:order_id>/', customer_order_detail, name='customer_order_detail'),
    path('cancel/<int:order_id>/', cancel_order, name='cancel_order'),
    path('<int:order_id>/chat/', chat_order, name='chat_order'),

]
