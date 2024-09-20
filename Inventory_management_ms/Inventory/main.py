from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel

app = FastAPI()

redis = get_redis_connection(
    host = "host_name",
    port = "port_number",
    password = "password",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database: redis


@app.post('/products', response_model=Product) 
def create(product: Product):
    return product.save()


@app.get('/products', response_model=list[Product]) 
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)
    return {
        'id' : product.pk,
        'name' : product.name,
        'price' : product.price,
        'quantity' : product.quantity
    }


@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)