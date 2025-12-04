from django import forms
from .models import Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nama_makanan', 'deskripsi', 'harga', 'foto_makanan', 'status']
