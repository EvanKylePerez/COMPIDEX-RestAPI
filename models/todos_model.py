from pydantic import BaseModel

class User(BaseModel):
    userName: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: str
    userStatus: str

class Merchant(BaseModel):
    businessName: str
    country: str
    status: str