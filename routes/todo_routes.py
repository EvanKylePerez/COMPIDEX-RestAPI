import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from config.database import merchants_data, products_data, users_data
from models.todos_model import Merchant, Product
from schemas.todos_schema import merchant_serializer, merchants_serializer, product_serializer, products_serializer, serializeListMerchants, serializeListProducts
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


@merchant_api_router.get("/merchant")
async def find_all_merchants():
    return serializeListMerchants(merchants_data.find())

# merchant GET methods by Query
@merchant_api_router.get("/merchant/findByName")
async def get_merchant_by_business_name(q: str | None = None):
    merchant = merchant_serializer(merchants_data.find_one({"businessName": q}))
    return {"status": "ok", "data": merchant}

@merchant_api_router.get("/merchant/findByCountry")
async def get_merchant_by_country(q: str | None = None):
    return serializeListMerchants(merchants_data.find({"country": (q)}))

@merchant_api_router.get("/merchant/findByStatus")
async def get_merchant_by_status(q: str | None = None):
    return serializeListMerchants(merchants_data.find({"status": (q)}))

# merchant GET methods
@merchant_api_router.get("/merchant/{id}")
async def get_merchant(id: str):
    merchant = merchants_serializer(merchants_data.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": merchant}

# merchant POST methods
@merchant_api_router.post("/merchant")
async def post_merchant(merchant: Merchant, _ = Depends(get_current_username)):
    _id = merchants_data.insert_one(dict(merchant))
    merchant = merchants_serializer(merchants_data.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data": merchant}

# merchant PUT methods
@merchant_api_router.put("/merchant/{id}")
async def update_merchant(id: str, merchant: Merchant, _ = Depends(get_current_username)):
    merchants_data.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(merchant)
    })
    merchant = merchants_serializer(merchants_data.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": merchant}

# merchant DELETE methods
@merchant_api_router.delete("/merchant/{id}")
async def delete_merchant(id: str, _ = Depends(get_current_username)):
    merchants_data.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok", "data": []}


product_api_router = APIRouter(tags=["Product"])


@product_api_router.get("/product")
async def find_all_products():
    return serializeListProducts(products_data.find())

# product GET methods by Query
@product_api_router.get("/product/findByCateg")
async def get_product_by_category(q: str | None = None):
    return serializeListProducts(products_data.find({"category": (q)}))

@product_api_router.get("/product/findByType")
async def get_product_by_type(q: str | None = None):
    return serializeListProducts(products_data.find({"productType": (q)}))

@product_api_router.get("/product/findByAvail")
async def get_product_by_availability(q: str | None = None):
    return serializeListProducts(products_data.find({"availability": (q)}))

@product_api_router.get("/product/findByCond")
async def get_product_by_condition(q: str | None = None):
    return serializeListProducts(products_data.find({"condition": (q)}))

@product_api_router.get("/product/findByPrice")
async def get_product_by_price(q: str | None = None):
    return serializeListProducts(products_data.find({"price": (q)}))

# product GET by ID method
@product_api_router.get("/product/{id}")
async def get_product(id: str):
    product = products_serializer(products_data.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": product}

# product POST method
@product_api_router.post("/product")
async def post_product(product: Product, _ = Depends(get_current_username)):
    _id = products_data.insert_one(dict(product))
    product = products_serializer(products_data.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data": product}

# product PUT method
@product_api_router.put("/product/{id}")
async def update_product(id: str, product: Product, _ = Depends(get_current_username)):
    products_data.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(product)
    })
    product = products_serializer(products_data.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": product}

# product DELETE method
@product_api_router.delete("/product/{id}")
async def delete_product(id: str, _ = Depends(get_current_username)):
    products_data.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok", "data": []}