from django.urls import path
from .views import home, menu_items, add_menu_item, delete_menu_item, edit_menu_item
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),  # Add this line for the homepage
    path('menu/', menu_items, name='menu_items'),
    path('menu/add/', add_menu_item, name='add_menu_item'),
    path('login/', auth_views.LoginView.as_view(template_name='webapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menu/delete/<int:item_id>/', delete_menu_item, name='delete_menu_item'),
    path('menu/edit/<int:item_id>/', edit_menu_item, name='edit_menu_item')
          
]
