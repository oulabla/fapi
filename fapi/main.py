from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Union
from fapi.view_models import *

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/items/{item_id}")
async def read_item(item_id : int):
    return {
        "item_id": item_id
    }


####################################################
@app.get("/api/products/{type}/{id}")
async def read_product(type: ProductType, id : int):
    if type == ProductType.standard:
        product = ProductStandardModel(**{
            "id": id,
            "name": "product",
            "description": "some desc",
            "price": 99.1231,
            "supplier": "Vasya",
        })
    elif type == ProductType.custom:
        product = ProductCustomModel(**{
            "id": id,
            "name": "product",
            "description": "some desc",
            "price": 99.1231,
            "info": "Custom",
        })

    return product

@app.post("/api/products/{type}")
async def insert_item(type: ProductType, product: ProductModel):
    product.type = type
    return product

@app.get("/api/products/")
async def list_item(offset: int = 0, limit: int = 10):
    return [{
        "name": "name",
        "item_id": 1
    }]