from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    preparation_time = models.IntegerField(default=10) # Newfield in minutes

    def __str__(self):
        return self.name
    
# Shopping Cart
class CartItem(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def subtotal(self):
        return self.menu_item.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} * {self.menu_item.name} ({self.user.username})"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    estimated_ready_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
