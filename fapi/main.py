from time import process_time, time
from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str


fake_users_db = {
    "oulala": {
        "username": "PapaTHeGreat",
        "full_name": "Ilya Pushkov",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashed1",
        "disabled": False,
    },
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


app = FastAPI()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_hash_password(password: str):
    return "fakehashed" + password


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/")
async def root():
    return {"message": "Hello World 1 asdas das "}


@app.get("/api/items/{item_id}/")
async def read_item(item_id : int, token: str = Depends(oauth2_scheme)):
    return {
        "item_id": item_id,
        "token": token
    }


# ####################################################
# @app.get("/api/products/{type}/{id}", response_model=ProductModel)
# async def read_product(type: ProductType, id : int, service: UsefulService = Depends(UsefulService)): 

#     product_base = {
#             "id": id,
#             "name": "product",
#             "description": "some desc",
#             "price": 99.1231,
#             "supplier": "Vasya",
#     }
#     product_base.update(await service.test())

#     if type == ProductType.standard:
#         product_base.update({
#             "supplier" : "Vasek"
#         })
#         product = ProductStandardModel(**product_base)
#     elif type == ProductType.custom:
#         product_base.update({
#             "info" : "Some infoi"
#         })
#         product = ProductStandardModel(**product_base)


#     return product

# @app.post("/api/products/{type}")
# async def insert_item(type: ProductType, product: ProductModel):
#     product.type = type
#     return product

# @app.get("/api/products/")
# async def list_item(offset: int = 0, limit: int = 10):
#     return [{
#         "name": "name",
#         "item_id": 1
#     }]

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)