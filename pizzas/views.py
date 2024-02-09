from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

pizzas = [{"Name": "Margherita", "Toppings": ["tomato sauce", "Mozzarella Cheese", "Fresh Basil"]},
          {"Name": "Pepperoni", "Toppings": ["tomato sauce", "Mozzarella Cheese", "Pepperoni"]}]

# GET request to send available pizzas
@api_view(['GET'])
def get_pizzas(request):
    return Response(pizzas)

# POST request to update pizzas
@api_view(['POST'])
def add_pizza(request):
    new_pizza = request.data

    # Check if pizza already exists based on a specific key
    for pizza in pizzas:
        if pizza["Name"].lower() == new_pizza["Name"].lower():
            return Response("Pizza with the same name already exists", status=status.HTTP_400_BAD_REQUEST)

    # If the pizza doesn't exist, add it to the list
    pizzas.append(new_pizza)
    return Response(request.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_pizza(request):
    pizza = request.data

    # Check if pizza already exists and remove it if present
    if pizza in pizzas:
        pizzas.remove(pizza)
        return Response(request.data, status=status.HTTP_200_OK)
    else:
        return Response("Pizza Not Present", status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def edit_pizza(request):
    oldPizza = request.data["oldPizza"]
    newPizza = request.data["newPizza"]

    for index, pizza in enumerate(pizzas):
        if pizza["Name"].lower() == oldPizza.lower():
            # Check if the new pizza name already exists
            if "Name" in newPizza and newPizza["Name"].lower() in (p["Name"].lower() for p in pizzas if p != pizza):
                return Response("New pizza name already exists.", status=status.HTTP_400_BAD_REQUEST)

            # Update pizza name if it's being changed
            if "Name" in newPizza:
                pizzas[index]["Name"] = newPizza["Name"]

            # Update toppings if they're being changed
            if "Toppings" in newPizza:
                pizzas[index]["Toppings"] = newPizza["Toppings"]

            return Response(request.data, status=status.HTTP_200_OK)

    return Response("Old pizza not found.", status=status.HTTP_400_BAD_REQUEST)
