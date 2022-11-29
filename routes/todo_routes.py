from fastapi import APIRouter
from config.database import collection_name
from models.todos_model import User, Merchant
from schemas.todos_schema import user_serializer, users_serializer, merchant_serializer, merchants_serializer
from bson import ObjectId

user_api_router = APIRouter(tags=["User"])

# user GET methods
@user_api_router.get("/user")
async def get_users():
    user = users_serializer(collection_name.find())
    return {"status": "ok", "data": user}

@user_api_router.get("/user/{id}")
async def get_user(id: str):
    user = users_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": user}

# user POST methods
@user_api_router.post("/user")
async def post_user(user: User):
    _id = collection_name.insert_one(dict(user))
    user = users_serializer(collection_name.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data": user}

# user PUT methods
@user_api_router.put("/user/{id}")
async def update_user(id: str, user: User):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    user = users_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": user}

# user DELETE methods
@user_api_router.delete("/user/{id}")
async def delete_user(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok", "data": []}


merchant_api_router = APIRouter(tags=["Merchant"])

# merchant GET methods
@merchant_api_router.get("/merchant/{id}")
async def get_merchant(id: str):
    merchant = merchants_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": merchant}

# merchant GET methods by Query
@merchant_api_router.get("/merchant/findByBusinessName")
async def get_merchant_by_business_name(q: str | None = None):
    merchant = merchant_serializer(collection_name.find_one({"businessName": q}))
    return {"status": "ok", "data": merchant}

@merchant_api_router.get("/merchant/findByCountry")
async def get_merchant_by_country(q: str | None = None):
    merchant = merchant_serializer(collection_name.find_one({"country": q}))
    return {"status": "ok", "data": merchant}

# merchant POST methods
@merchant_api_router.post("/merchant")
async def post_merchant(merchant: Merchant):
    _id = collection_name.insert_one(dict(merchant))
    merchant = merchants_serializer(collection_name.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data": merchant}

# merchant PUT methods
@merchant_api_router.put("/merchant/{id}")
async def update_merchant(id: str, merchant: Merchant):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(merchant)
    })
    merchant = merchants_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": merchant}

# merchant DELETE methods
@merchant_api_router.delete("/merchant/{id}")
async def delete_merchant(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok", "data": []}