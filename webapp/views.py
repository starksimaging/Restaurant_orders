from django.shortcuts import render, redirect
from django.utils.timezone import now, timedelta, localtime
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import MenuItem, CartItem
from .forms import MenuItemForm
from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import CheckoutForm
from .models import CartItem, Order
from django.utils.timezone import make_aware
from datetime import datetime
# Create your views here.
# @login_required commented out unless you want to restrict access to the menu items to only logged in users
def menu_items(request):
    items = MenuItem.objects.all()
    return render(request, 'webapp/menu_items.html', {'items': items})


def home(request):
    return render(request, 'webapp/home.html')
# Add this function to add menu items
@staff_member_required
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES) # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('menu_items')
    else:
        form = MenuItemForm()

        return render(request, 'webapp/add_menu_item.html', {'form': form})
# Add this function to delete menu items
@staff_member_required
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
@staff_member_required
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

# Shopping cart view and logic
@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, menu_item=menu_item)

    if not created:
        cart_item.quantity = +1
        cart_item.save()

    return redirect('view_cart')

#This function is to view the cart
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.subtotal() for item in cart_items)

    return render(request, 'webapp/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


#This function is to remove items from the cart
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404( CartItem, user=request.user, menu_item_id=item_id)
    cart_item.delete()
    return redirect('view_cart')

# User Registration View

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after successful registration
            return redirect('home')  # Redirect to home page after registration
        else:
            messages.error(request, "Registration failed. Please check your details.")
    else:
        form = UserRegisterForm()
    
    return render(request, 'webapp/register.html', {'form': form})


# Checkout view
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.subtotal() for item in cart_items)

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    max_prep_time = max((item.menu_item.preparation_time for item in cart_items), default=10)
    current_time = make_aware(datetime.now())
    estimated_ready_time = current_time + timedelta(minutes=max_prep_time)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create an order
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                estimated_ready_time=estimated_ready_time
            )

            # Clear the cart
            cart_items.delete()

            return render(request, 'webapp/checkout_success.html', {'order': order})
    else:
        form = CheckoutForm()

    return render(request, 'webapp/checkout.html', {'total_price': total_price, 'estimated_ready_time': estimated_ready_time, 'form': form})