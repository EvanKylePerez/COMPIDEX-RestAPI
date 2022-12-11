# JSON serialized from model
def merchant_serializer(merchant) -> dict:
    return {
        "id": str(merchant["_id"]),
        "businessName": merchant["businessName"],
        "country": merchant["country"],
        "status": merchant["status"]
    }

# Returns objects in list form
def merchants_serializer(merchants) -> list:
    return [merchant_serializer(merchant) for merchant in merchants]

# Serializes each object-list index into dict format, if index 'i' is equal to ObjectId.
# Index automates to making an empty list instead, if index is 'i' not equal to ObjectId.
def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

# Returns formatted object dict format into list form
def serializeListMerchants(merchants) -> list:
    return [serializeDict(a) for a in merchants]

def product_serializer(product) -> dict:
    return {
        "id": str(product["_id"]),
        "title": product["title"],
        "brand": product["brand"],
        "category": product["category"],
        "productType": product["productType"],
        "description": product["description"],
        "specification": product["specification"],
        "vendorUrl": product["vendorUrl"],
        "availability": product["availability"],
        "condition": product["condition"],
        "price": product["price"],
        "installment": product["installment"],
        "subscriptionCost": product["subscriptionCost"]
    }

def products_serializer(products) -> list:
    return [product_serializer(product) for product in products]

def serializeListProducts(products) -> list:
    return [serializeDict(a) for a in products]