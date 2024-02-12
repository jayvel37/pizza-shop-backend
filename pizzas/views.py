from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pizza, PizzaTopping

# GET request to send available pizzas
@api_view(['GET'])
def get_pizzas(request):
    # Retrieve all pizza instances from the database
    pizzas = Pizza.objects.all()

    # Prepare the response data by iterating over each pizza instance, including its name and associated toppings
    data = [{'Name': pizza.name, 'Toppings': [topping.topping_name for topping in pizza.pizzatopping_set.all()]} for
            pizza in pizzas]

    # Return the response containing the pizza data
    return Response(data)

@api_view(['POST'])
def add_pizza(request):
    # Extract data from request
    name = request.data.get('Name')
    toppings = request.data.get('Toppings', [])

    # Validate request data
    if not name:
        return Response("Missing 'Name' field in request data", status=status.HTTP_400_BAD_REQUEST)
    if not toppings:
        return Response("Missing 'Toppings' field in request data", status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if the pizza name already exists
        print(Pizza.objects.filter(name=name).exists())
        if Pizza.objects.filter(name=name).exists():
            return Response("Pizza with this name already exists", status=status.HTTP_400_BAD_REQUEST)

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
        # Attempt to get the pizza instance by name from the request data
        pizza_name = request.data.get('Name')
        pizza = Pizza.objects.get(name=pizza_name)
    except Pizza.DoesNotExist:

        # If the pizza with the provided name does not exist, return a 400 response
        return Response("Pizza Not Present", status=status.HTTP_400_BAD_REQUEST)

    # If pizza exists, delete it from the database
    pizza.delete()

    # Return a success response upon successful deletion
    return Response(status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_pizza(request):
    try:
        # Get the old pizza instance by name
        old_pizza_name = request.data.get("oldPizza")
        old_pizza = Pizza.objects.get(name=old_pizza_name)
    except Pizza.DoesNotExist:
        return Response("Pizza not found.", status=status.HTTP_400_BAD_REQUEST)

    # Extract updated data from request
    new_name = request.data.get('newPizza', {}).get('Name')
    new_toppings = request.data.get('newPizza', {}).get('Toppings', [])

    try:
        # Update pizza name if provided
        if new_name:
            old_pizza.name = new_name
            old_pizza.save()

        # Update toppings if provided
        if new_toppings:

            # Delete existing toppings
            old_pizza.pizzatopping_set.all().delete()

            # Create new toppings
            for topping_name in new_toppings:
                PizzaTopping.objects.create(pizza=old_pizza, topping_name=topping_name)

        return Response("Pizza updated successfully", status=status.HTTP_200_OK)
    except Exception as e:
        return Response(f"Error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)