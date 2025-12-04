from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']
