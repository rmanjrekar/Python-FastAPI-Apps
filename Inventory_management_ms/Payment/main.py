from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.background import BackgroundTasks
from starlette.requests import Request
import requests
import time

app = FastAPI()

redis = get_redis_connection(
    host = "host_name",
    port = "port_number",
    password = "password",
    decode_responses=True
)

class Order(HashModel):
    product_id : str
    price : float
    fee : float
    total : float
    quantity : int
    status : str

    class Meta:
        database: redis


@app.get('/orders/{pk}')
def get_order(pk: str):
    return Order.get(pk)


@app.post('/orders')
async def create(request: Request, background_task: BackgroundTasks):
    body = await request.json()
    req = requests.get('http://localhost:8000/products/%s' % body['id'])

    product = req.json()

    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.2 * product['price'],       # 20% of the product price
        total = 1.2 * product['price'],     # price + fee which means it is 1.2 times product price 
        quantity = body['quantity'],
        status = 'pending'
    )
    order.save()

    background_task.add_task(order_completed, order)
    return order

'''
to change the status of the order from 'pending' to 'completed'
'''
def order_completed(order: Order):
    time.sleep(5)   # Added sleep to add a delay before changing the status from 'pending' to 'completed'
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')