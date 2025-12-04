# orders/models.py

from django.db import models
from django.contrib.auth.models import User
# Mengimpor model dari aplikasi lain (Asumsi Menu dan RestaurantProfile ada di restaurant.models)
from restaurant.models import Menu, RestaurantProfile 
from accounts.models import DriverProfile

# 1. DEFINISIKAN STATUS_CHOICES DI LEVEL MODUL (LUAR KELAS)
STATUS_CHOICES = [
    ('pending', 'Menunggu Konfirmasi'),
    ('processing', 'Diproses'),
    ('ready', 'Siap Diambil'),
    ('on_delivery', 'Dalam Pengiriman'),
    ('completed', 'Selesai'),
]


# 2. GABUNGKAN DEFINISI KELAS ORDER MENJADI SATU
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)
    total_harga = models.IntegerField()
    # Menggunakan STATUS_CHOICES yang didefinisikan di atas
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 
    created_at = models.DateTimeField(auto_now_add=True)


    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    def __str__(self):
        return f"Order #{self.id} - {self.restaurant.nama_restoran}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu.nama_makanan} x {self.qty}"
    
class ChatMessage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="chat")
    pengirim = models.ForeignKey(User, on_delete=models.CASCADE)
    isi_pesan = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pengirim.username}: {self.isi_pesan[:30]}"
    

class OrderChat(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # siapa pengirim
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
