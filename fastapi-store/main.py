import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel
import requests

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host='redis-17759.c15.us-east-1-2.ec2.cloud.redislabs.com',
    port=17759,
    password='vJ6xEKrCwx3uEk8mcjvwwzyMrzKkgadu',
    decode_responses=True
)

# First Dat Type: i.e. what we send to the API
class ProductOrder(HashModel):
    product_id: str
    quantity: int
    class Meta:
        database = redis

class ProductOrderRequest(BaseModel):
    product_id: str
    quantity: int

# Second Data Type: i.e. what we get from the API
class ProductOrderResponse(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str
    class Meta:
        database = redis

@app.post("/orders", response_model=None)
async def new_order(order: ProductOrderRequest, background_tasks: BackgroundTasks):
    product_order = ProductOrder(product_id=order.product_id, quantity=order.quantity)
    req = requests.get(f'http://localhost:8000/product/{product_order.product_id}')
    product = req.json()
    fee = product['price'] * 0.2

    order = ProductOrderResponse(
        product_id=product_order.product_id,
        price=product['price'],
        fee=fee,
        total=(product['price'] + fee) * product_order.quantity,
        quantity=product_order.quantity,
        status='pending'
    )
    order.save()
    background_tasks.add_task(order_complete, order)

    return order

@app.get("/orders/{product_id}", response_model=None)
async def order(product_id: str):
    return format(product_id)

@app.get("/orders", response_model=None)
async def all_orders():
    return [format(pk) for pk in ProductOrderResponse.all_pks()]

def format(pk: str):
    order = ProductOrderResponse.get(pk)
    return {
        'product_id': order.product_id,
        'price': order.price,
        'fee': order.fee,
        'total': order.total,
        'quantity': order.quantity,
        'status': order.status
    }

def order_complete(order: ProductOrderResponse):
    '''
    This method changes the order fron pending to complete after sleeping for 5 seconds to 
    simulate a real world scenario. We use redis streams to tell the warehouse microservice
    that the order is completed.
    '''
    time.sleep(5)
    order.status = 'complete'
    redis.xadd('order-completed', order.__dict__)