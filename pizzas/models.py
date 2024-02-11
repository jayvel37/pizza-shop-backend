from django.db import models

class Pizza(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class PizzaTopping(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    topping_name = models.CharField(max_length=100)

    class Meta:
        unique_together = (('pizza', 'topping_name'),)