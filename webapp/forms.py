from django import forms
from .models import MenuItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

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

# Credit card form using RegexValidator
class CheckoutForm(forms.Form):
    card_number = forms.CharField(
        label='card_number',
        max_length=25,
        validators=[
            RegexValidator(
                regex=r'^\d{4} \d{4} \d{4} \d{4}|\d{16}$',
                message='Please enter a valid credit card number'
            )
            
        ]
    )
    expiration_date = forms.CharField(
        label='Expiration Date (mm/yy)',
        max_length=5,
        validators=[
            RegexValidator(
                regex=r'^(0[1-9]|1[0-2])\/\d{2}$',
                message='Enter a valid expiration date in MM/YY format',
            )
                

                    

        ]
    )
    cvv = forms.CharField(
        label='CVV',
        max_length=3,
        validators=[
            RegexValidator(
                regex=r'^\d{3,4}$',
                message='Enter a valid CVV code'
            )
        ]
    )





    