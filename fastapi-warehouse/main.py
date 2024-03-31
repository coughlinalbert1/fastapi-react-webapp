from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel
from typing import List

app = FastAPI()

origins = [
    "http://localhost:3000",
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

class ProductModel(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

class Product(BaseModel):
    name: str
    price: float
    quantity: int


@app.get("/product/{product_id}", response_model=None)
async def get_product(product_id: str):
    product = ProductModel.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "id": product.pk, 
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }

@app.get("/products", response_model=None)
async def get_products():
    keys = redis.scan_iter("*")
    if not keys:
        raise HTTPException(status_code=404, detail="No products found")
    return [
        {
            "id": product.pk,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        }
        for key in keys if 'ProductModel' in key 
        for product in [ProductModel.get(key.split(":")[-1])]
    ]
  

@app.post("/product", response_model=None)
async def create_product(product: Product):
    product_model = ProductModel(**product.model_dump())
    product_model.save()
    return {
        "id": product_model.pk,
        "name": product_model.name,
        "price": product_model.price,
        "quantity": product_model.quantity
    }

@app.delete("/product/{product_id}", response_model=None)
async def delete_product(product_id: str):
    product = ProductModel.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    ProductModel.delete(product_id)
    return 1


