from pydantic import BaseModel
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

class Merchant(BaseModel):
    businessName: str
    country: str
    status: str

class Product(BaseModel):
    title: str
    brand: str
    category: str
    productType: str
    description: str
    specification: str
    vendorUrl: str
    availability: str
    condition: str
    price: str
    installment: str
    subscriptionCost: str
