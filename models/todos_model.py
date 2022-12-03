from pydantic import BaseModel

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
