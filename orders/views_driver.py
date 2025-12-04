from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import DriverProfile
from .models import Order
from django.contrib import messages

@login_required
def driver_dashboard(request):
    driver = DriverProfile.objects.get(user=request.user)
    ongoing = Order.objects.filter(driver=driver, status="delivering").count()
    finished = Order.objects.filter(driver=driver, status="finished").count()

    return render(request, "driver/dashboard.html", {
        "ongoing": ongoing,
        "finished": finished
    })

@login_required
def ready_orders(request):
    orders = Order.objects.filter(status="processing", driver__isnull=True)
    return render(request, "driver/ready_orders.html", {"orders": orders})

@login_required
def take_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    driver = DriverProfile.objects.get(user=request.user)

    if order.driver is not None:
        messages.error(request, "Pesanan sudah diambil driver lain!")
        return redirect("driver_ready_orders")

    order.driver = driver
    order.status = "delivering"
    order.save()

    messages.success(request, "Pesanan berhasil diambil!")
    return redirect("driver_my_orders")


@login_required
def my_orders(request):
    driver = DriverProfile.objects.get(user=request.user)
    orders = Order.objects.filter(driver=driver).exclude(status="finished")
    return render(request, "driver/my_orders.html", {"orders": orders})


@login_required
def finish_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.driver.user != request.user:
        messages.error(request, "Anda tidak berhak menyelesaikan pesanan ini.")
        return redirect("driver_my_orders")

    order.status = "finished"
    order.save()

    messages.success(request, "Pesanan selesai!")
    return redirect("driver_my_orders")


