# pizza-shop-backend
Django backend for pizza shop app where owner can update toppings and chefs can update pizza menu with new pizzas. Using postgreSQL database for data storage and retrieval. 

Logins:

- Admin user: admin@pizzas.com

- Admin Password: adminPassword

- Chef user: chef@pizzas.com

- Chef password: pizzaPassword

Admin will take user to the owner/admin page where both toppings and pizzas can be edited.

Chef will login user as a chef where only pizzas can be updated.

Tests:

- Click the add button to open the modal window to enter new topping/pizza. (Duplicates not allowed)
- Click the edit button to open the modal window to edit topping/pizza.
- Click the delete button to delete a topping/pizza.
- Note: Click the submit button in modal window with empty fields to get appropriate popup prompting user to enter field.

Api tests:
- If wanting to test API's by themselves mock JSON data in postman, insomnia, etc.
