from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_suspended = models.BooleanField(default=False)  # baru
    is_deleted = models.BooleanField(default=False)    # baru

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

class RestaurantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nama_restoran = models.CharField(max_length=100)
    alamat = models.TextField()
    deskripsi = models.TextField(blank=True)

    jam_buka = models.TimeField()
    jam_tutup = models.TimeField()

    status_buka = models.BooleanField(default=True)

    foto_logo = models.ImageField(upload_to='logo_restoran/', blank=True, null=True)

    kategori = models.CharField(
        max_length=50,
        blank=True,
        help_text="Contoh: Ayam, Kopi, Burger, dll"
    )

    def __str__(self):
        return self.nama_restoran

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alamat = models.TextField(blank=True)
    nomor_telepon = models.CharField(max_length=15, blank=True)
    foto_profil = models.ImageField(upload_to='profil_customer/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Customer"


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nomor_telepon = models.CharField(max_length=15)
    plat_kendaraan = models.CharField(max_length=20)
    jenis_kendaraan = models.CharField(max_length=50)
    status_aktif = models.BooleanField(default=True)
    foto_profil = models.ImageField(upload_to='profil_driver/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Driver ({self.plat_kendaraan})"





# class Menu(models.Model):

#     STATUS_CHOICES = (
#         ('available', 'Available'),
#         ('sold_out', 'Sold Out'),
#     )

#     restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)

#     nama_makanan = models.CharField(max_length=100)
#     deskripsi = models.TextField(blank=True)
#     harga = models.DecimalField(max_digits=10, decimal_places=2)

#     foto_makanan = models.ImageField(upload_to='foto_makanan/', blank=True, null=True)

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

#     def __str__(self):
#         return self.nama_makanan

