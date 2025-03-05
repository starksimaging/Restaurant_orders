from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MenuItem
from .forms import MenuItemForm
from django.shortcuts import get_object_or_404

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

@login_required
def delete_menu_item(request, item_id):
    # Ensure item_id is an integer
    try:
        item_id = int(item_id)
    except ValueError:
        return render(request, "webapp/error.html", {"message": "Invalid item ID"})

    # Fetch the menu item
    item = get_object_or_404(MenuItem, id=item_id)

    if request.method == "POST":
        item.delete()
        return redirect("menu_items")  # Redirect to menu list after deletion

    return render(request, "webapp/delete_menu_item.html", {"item": item})


# Add this function to edit menu items
@login_required
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save() # Ensure the form is saved before redirecting
            return redirect('menu_items') # Redirect to the menu list after saving
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'webapp/edit_menu_item.html', {'form': form})