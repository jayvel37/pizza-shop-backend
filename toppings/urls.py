from django.urls import path
from . import views

urlpatterns = [
    path('get-toppings/', views.get_toppings),
    path('add-topping/', views.add_topping),
    path('delete-topping/', views.delete_topping),
    path('edit-topping/', views.edit_topping),
]
