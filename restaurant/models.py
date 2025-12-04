from django.db import models
from accounts.models import Profile, RestaurantProfile
from django.contrib.auth.models import User
class Menu(models.Model):

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold_out', 'Sold Out'),
    )

    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)

    nama_makanan = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True)
    harga = models.DecimalField(max_digits=10, decimal_places=2)

    foto_makanan = models.ImageField(upload_to='foto_makanan/', blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.nama_makanan


# class Order(models.Model):

#     STATUS_CHOICES = [
#         ('diterima', 'Diterima'),
#         ('diproses', 'Diproses'),
#         ('menunggu_driver', 'Menunggu Driver'),
#         ('dikirim', 'Dikirim'),
#         ('selesai', 'Pesanan Selesai'),
#         ('dibatalkan', 'Pesanan Dibatalkan'),
#     ]

#     customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='diterima')

#     total_harga = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order #{self.id} - {self.restaurant.nama_restoran}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

#     qty = models.PositiveIntegerField(default=1)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.menu.nama_makanan} x {self.qty}"


class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart milik {self.customer.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    qty = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu.nama_makanan} x {self.qty}"