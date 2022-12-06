import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from config.database import collection_name
from models.todos_model import Merchant, Product
from schemas.todos_schema import merchant_serializer, merchants_serializer, product_serializer, products_serializer, serializeDict, serializeList
from bson import ObjectId
from typing import List

user_api_router = APIRouter(tags=["User"])

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"compidex2022"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@user_api_router.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}



merchant_api_router = APIRouter(tags=["Merchant"])


# merchant GET methods by Query

@merchant_api_router.get("/merchant")
async def find_all_merchants():
    return serializeList(collection_name.find())

@merchant_api_router.get("/merchant/findByName")
async def get_merchant_by_business_name(q: str | None = None):
    merchant = merchant_serializer(collection_name.find_one({"businessName": q}))
    return {"status": "ok", "data": merchant}

@merchant_api_router.get("/merchant/findByCountry")
async def get_merchant_by_country(q: str | None = None):
    merchant = merchant_serializer(collection_name.find({"country": q}))
    return {"status": "ok", "data": merchant}

@merchant_api_router.get("/merchant/findByStatus")
async def get_merchant_by_status(q: str | None = None):
    merchant = merchant_serializer(collection_name.find_one({"status": q}))
    return {"status": "ok", "data": merchant}

# merchant GET methods
@merchant_api_router.get("/merchant/{id}")
async def get_merchant(id: str):
    merchant = merchants_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": merchant}

# merchant POST methods
@merchant_api_router.post("/merchant")
async def post_merchant(merchant: Merchant, _ = Depends(get_current_username)):
    _id = collection_name.insert_one(dict(merchant))
    merchant = merchants_serializer(collection_name.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data": merchant}

# merchant PUT methods
@merchant_api_router.put("/merchant/{id}")
async def update_merchant(id: str, merchant: Merchant, _ = Depends(get_current_username)):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(merchant)
    })
    merchant = merchants_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": merchant}

# merchant DELETE methods
@merchant_api_router.delete("/merchant/{id}")
async def delete_merchant(id: str, _ = Depends(get_current_username)):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok", "data": []}


product_api_router = APIRouter(tags=["Product"])


# product GET methods by Query
@product_api_router.get("/product/findByCateg")
async def get_product_by_category(q: str | None = None):
    product = product_serializer(collection_name.find_one({"category": q}))
    return {"status": "ok", "data": product}

@product_api_router.get("/product/findByType")
async def get_product_by_type(q: str | None = None):
    product = product_serializer(collection_name.find_one({"productType": q}))
    return {"status": "ok", "data": product}

@product_api_router.get("/product/findByAvail")
async def get_product_by_availability(q: str | None = None):
    product = product_serializer(collection_name.find_one({"availability": q}))
    return {"status": "ok", "data": product}

@product_api_router.get("/product/findByCond")
async def get_product_by_condition(q: str | None = None):
    product = product_serializer(collection_name.find_one({"condition": q}))
    return {"status": "ok", "data": product}

@product_api_router.get("/product/findByPrice")
async def get_product_by_price(q: str | None = None):
    product = product_serializer(collection_name.find_one({"price": q}))
    return {"status": "ok", "data": product}

# product GET by ID method
@product_api_router.get("/product/{id}")
async def get_product(id: str):
    product = products_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": product}

# product POST method
@product_api_router.post("/product")
async def post_product(product: Product, _ = Depends(get_current_username)):
    _id = collection_name.insert_one(dict(product))
    product = products_serializer(collection_name.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data": product}

# product PUT method
@product_api_router.put("/product/{id}")
async def update_product(id: str, product: Product, _ = Depends(get_current_username)):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(product)
    })
    product = products_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": product}

# product DELETE method
@product_api_router.delete("/product/{id}")
async def delete_product(id: str, _ = Depends(get_current_username)):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok", "data": []}