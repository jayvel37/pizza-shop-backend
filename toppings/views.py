from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Topping

#toppings = ['Thin Crust','Marinara Sauce', 'Mozzerella Cheese', 'Pepperoni']
# GET request to send available toppings
@api_view(['GET'])
def get_toppings(request):
    toppings = Topping.objects.all().values('name')
    results = []
    for topping in toppings:
        results.append(topping['name'])
    print(list(results))
    return Response({'Toppings': list(results)})

@api_view(['POST'])
def add_topping(request):
    new_topping_name = request.data.get("Topping")
    if not new_topping_name:
        return Response("Invalid request: 'Topping' field is missing", status=status.HTTP_400_BAD_REQUEST)

    try:
        new_topping = Topping.objects.create(name=new_topping_name)
        return Response({'Topping': new_topping.name}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response("Topping already exists", status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_topping(request):
    topping_name = request.data.get("Topping")
    if not topping_name:
        return Response("Invalid request: 'Topping' field is missing", status=status.HTTP_400_BAD_REQUEST)

    try:
        topping = Topping.objects.get(name=topping_name)
        topping.delete()
        return Response({'Topping': topping_name}, status=status.HTTP_200_OK)
    except Topping.DoesNotExist:
        return Response("Topping not found", status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def edit_topping(request):
    old_topping_name = request.data.get("oldTopping")
    new_topping_name = request.data.get("newTopping")
    if not old_topping_name or not new_topping_name:
        return Response("Invalid request: 'oldTopping' or 'newTopping' field is missing", status=status.HTTP_400_BAD_REQUEST)

    try:
        topping = Topping.objects.get(name=old_topping_name)
        topping.name = new_topping_name
        topping.save()
        return Response({'Topping': new_topping_name}, status=status.HTTP_200_OK)
    except Topping.DoesNotExist:
        return Response("Topping not found", status=status.HTTP_400_BAD_REQUEST)

