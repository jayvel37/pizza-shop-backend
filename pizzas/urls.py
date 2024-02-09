from django.urls import path
from . import views

urlpatterns = [
    path('get-pizzas/', views.get_pizzas),
    path('add-pizza/', views.add_pizza),
    path('delete-pizza/', views.delete_pizza),
    path('edit-pizza/', views.edit_pizza),
]
