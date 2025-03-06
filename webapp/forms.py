from django import forms
from .models import MenuItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description', 'image', 'preparation_time'] # Add 'image' to the list of fields
        widgets = {
            'Description': forms.Textarea(attrs={'rows': 3}),
            'preparation_time': forms.NumberInput(attrs={'min': 1, 'step': 1}),
        }
        


# User registration form

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    fields = ['username', 'email', 'password', 'password2']

# Credit card form
class CheckoutForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16, min_length=16)
    expiration_date = forms.CharField(label= 'Expiration Date (MM/YY)', max_length=5)
    cvv = forms.CharField(label='CVV', max_length=3, min_length=3)
    