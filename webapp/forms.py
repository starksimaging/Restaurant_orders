from django import forms
from .models import MenuItem


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description', 'image'] # Add 'image' to the list of fields
        widgets = {
            'Description': forms.Textarea(attrs={'rows': 3})
        }
        