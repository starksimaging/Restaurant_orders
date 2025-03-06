from django.contrib import admin
from .models import MenuItem, Order

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'preparation_time')  # Fixed typo
    search_fields = ('name', 'description')
    list_filter = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'timestamp','estimated_ready_time')  # Fixed spaces
    search_fields = ('user__username',)
    list_filter = ('timestamp','estimated_ready_time')  # Fixed spaces