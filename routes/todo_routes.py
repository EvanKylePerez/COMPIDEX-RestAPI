from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.database import collection_name
from models.todos_model import User, UserInDB, Merchant, Product
from schemas.todos_schema import merchant_serializer, merchants_serializer, product_serializer, products_serializer
from bson import ObjectId

admin_user_db = {
    "admin": {
        "username": "admin",
        "full_name": "compidexAdmin",
        "email": "compidexsupport@gmail.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False
    }
}

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(admin_user_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

user_api_router = APIRouter(tags=["User"])

@user_api_router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = admin_user_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@user_api_router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


merchant_api_router = APIRouter(tags=["Merchant"])


# merchant GET methods by Query
@merchant_api_router.get("/merchant/findByBusinessName")
async def get_merchant_by_business_name(q: str | None = None):
    merchant = merchant_serializer(collection_name.find_one({"businessName": q}))
    return {"status": "ok", "data": merchant}

@merchant_api_router.get("/merchant/findByCountry")
async def get_merchant_by_country(q: str | None = None):
    merchant = merchant_serializer(collection_name.find_one({"country": q}))
    return {"status": "ok", "data": merchant}


# merchant GET methods
@merchant_api_router.get("/merchant/{id}")
async def get_merchant(id: str):
    merchant = merchants_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": merchant}

# merchant POST methods
@merchant_api_router.post("/merchant")
async def post_merchant(merchant: Merchant, _ = Depends(get_current_user)):
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


product_api_router = APIRouter(tags=["Product"])


# product GET methods by Query
@product_api_router.get("/product/findByCat")
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

@product_api_router.get("/product/findByCon")
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
async def post_product(product: Product):
    _id = collection_name.insert_one(dict(product))
    product = products_serializer(collection_name.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data": product}

# product PUT method
@product_api_router.put("/product/{id}")
async def update_product(id: str, product: Product):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(product)
    })
    product = products_serializer(collection_name.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": product}

# product DELETE method
@product_api_router.delete("/product/{id}")
async def delete_product(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok", "data": []}