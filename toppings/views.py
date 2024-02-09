import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

toppings = ['Thin Crust','Marinara Sauce', 'Mozzerella Cheese', 'Pepperoni']
# GET request to send available toppings
@api_view(['GET'])
def get_toppings(request):
    return Response({'Toppings': toppings})

@api_view(['POST'])
def add_topping(request):
    result = request.data["Topping"]
     # check if new topping in old results
    if result in toppings:
        return Response("Topping Already Exists", status=status.HTTP_400_BAD_REQUEST)
    else:
        toppings.append(result)
        print(toppings)
        return Response(request.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_topping(request):
    topping = request.data["Topping"]
     # check if new topping in old results
    if topping in toppings:
        toppings.remove(topping)
        return Response(request.data, status=status.HTTP_200_OK)
    else:
        return Response("Topping Not Present", status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_topping(request):
    oldTopping = request.data["oldTopping"]
    newTopping = request.data["newTopping"]
    index = toppings.index(oldTopping)
    if index > -1 and len(newTopping) > 0 and newTopping not in toppings:
        toppings[index] = newTopping
        return Response(request.data, status=status.HTTP_200_OK)
    else:
        return Response("Issue updating topping.", status=status.HTTP_400_BAD_REQUEST)
