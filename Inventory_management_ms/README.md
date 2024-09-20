This project is to create a simplified e-commerce order processing system using FastAPI and Redis. 
It also demonstrate Microservices architecture where two applications are running independently and communicating with each other.
This system handles product creation, order creation, order completion, and potential refunds. 

Here's an overview of how these code chunks work together:

Main Applications (main.py):
The main FastAPI application is defined in this file for both the application. 
It interacts with Redis to create products and process orders.

Inventory/main.py
The Product model is defined using the HashModel class, representing the product's attributes.
The '/products' route allows creating products, retrieving a list of all products, and retrieving a single product by its ID.

inventory_consumer.py
This script is a background worker that continuously consumes messages from the 'order_completed' Redis stream.
Each message contains information about a completed order, including the product ID and quantity.
The worker updates the product quantity based on the completed order's quantity.

Payment/main.py
The create route creates an order, calculates the price, fee, and total, and sets the order status to 'pending'.
A background task is added to simulate order completion with a delay and then changing the order status to 'completed'.
The '/orders' route allows creating orders and retrieving an order by its ID.

payment_consumer.py
This script is another background worker that consumes messages from the 'refund_order' Redis stream.
Each message contains information about an order that couldn't be completed (e.g., product deletion before completion).
The worker updates the status of these orders to 'refunded' in the Order model.
