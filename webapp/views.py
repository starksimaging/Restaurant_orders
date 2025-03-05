from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MenuItem
from .forms import MenuItemForm

# Create your views here.
def menu_items(request):
    items = MenuItem.objects.all()
    return render(request, 'webapp/menu_items.html', {'items': items})


def home(request):
    return render(request, 'webapp/home.html')

@login_required
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES) # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('menu_items')
    else:
        form = MenuItemForm()

        return render(request, 'webapp/add_menu_item.html', {'form': form})

