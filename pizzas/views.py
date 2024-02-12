from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pizza, PizzaTopping
from .serializers import PizzaSerializer


#pizzas = [{"Name": "Margherita", "Toppings": ["tomato sauce", "Mozzarella Cheese", "Fresh Basil"]},
#          {"Name": "Pepperoni", "Toppings": ["tomato sauce", "Mozzarella Cheese", "Pepperoni"]}]

# GET request to send available pizzas
@api_view(['GET'])
def get_pizzas(request):
    pizzas = Pizza.objects.all()
    data = [{'Name': pizza.name, 'Toppings': [topping.topping_name for topping in pizza.pizzatopping_set.all()]} for pizza in pizzas]
    return Response(data)

@api_view(['POST'])
def add_pizza(request):
    print(request.data)
    # Extract data from request
    name = request.data.get('Name')
    toppings = request.data.get('Toppings', [])

    # Validate request data
    if not name:
        return Response("Missing 'Name' field in request data", status=status.HTTP_400_BAD_REQUEST)
    if not toppings:
        return Response("Missing 'Toppings' field in request data", status=status.HTTP_400_BAD_REQUEST)

    try:
        # Create Pizza instance
        pizza = Pizza.objects.create(name=name)

        # Create PizzaTopping instances for each topping
        for topping_name in toppings:
            PizzaTopping.objects.create(pizza=pizza, topping_name=topping_name)

        return Response("Pizza added successfully", status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(f"Error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_pizza(request):
    try:
        pizza = Pizza.objects.get(name=request.data['Name'])
    except Pizza.DoesNotExist:
        return Response("Pizza Not Present", status=status.HTTP_400_BAD_REQUEST)
    pizza.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_pizza(request):
    try:
        old_pizza = Pizza.objects.get(name=request.data["Name"])
    except Pizza.DoesNotExist:
        return Response("Old pizza not found.", status=status.HTTP_400_BAD_REQUEST)

    serializer = PizzaSerializer(old_pizza, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)