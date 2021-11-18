from time import process_time, time
from fastapi import FastAPI, Depends, Request, Response
import uvicorn
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Union
from fapi.view_models import *
import asyncio

class UsefulService:
    async def test(self):
        await asyncio.sleep(0.2)
        return {"name":"test service"}

app = FastAPI()

app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time()
    response: Response = await call_next(request)
    process_time = time() - start_time
    
    
    response.headers["X-PROCESS-TIME"] = str(process_time)

################

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/items/{item_id}")
async def read_item(item_id : int):
    return {
        "item_id": item_id
    }


####################################################
@app.get("/api/products/{type}/{id}", response_model=ProductModel)
async def read_product(type: ProductType, id : int, service: UsefulService = Depends(UsefulService)): 

    product_base = {
            "id": id,
            "name": "product",
            "description": "some desc",
            "price": 99.1231,
            "supplier": "Vasya",
    }
    product_base.update(await service.test())

    if type == ProductType.standard:
        product_base.update({
            "supplier" : "Vasek"
        })
        product = ProductStandardModel(**product_base)
    elif type == ProductType.custom:
        product_base.update({
            "info" : "Some infoi"
        })
        product = ProductStandardModel(**product_base)


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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)