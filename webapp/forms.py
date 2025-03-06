from django import forms
from .models import MenuItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description', 'image'] # Add 'image' to the list of fields
        widgets = {
            'Description': forms.Textarea(attrs={'rows': 3})
        }
        


# User registration form

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    fields = ['username', 'email', 'password', 'password2']
    