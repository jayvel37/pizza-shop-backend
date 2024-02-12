from rest_framework import serializers
from .models import Pizza, PizzaTopping

class PizzaSerializer(serializers.ModelSerializer):
    toppings = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Pizza
        fields = ['Name', 'Toppings']

    def create(self, validated_data):
        toppings_data = validated_data.pop('toppings', [])
        pizza = Pizza.objects.create(**validated_data)
        for topping_name in toppings_data:
            PizzaTopping.objects.create(pizza=pizza, topping_name=topping_name)
        return pizza

class PizzaToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaTopping
        fields = ['pizza', 'topping_name']