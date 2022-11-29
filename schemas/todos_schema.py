def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "userName": user["userName"],
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "email": user["email"],
        "password": user["password"],
        "phone": user["phone"],
        "userStatus": user["userStatus"]
    }

def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]


def merchant_serializer(merchant) -> dict:
    return {
        "id": str(merchant["_id"]),
        "businessName": merchant["businessName"],
        "country": merchant["country"],
        "status": merchant["status"]
    }

def merchants_serializer(merchants) -> list:
    return [merchant_serializer(merchant) for merchant in merchants]

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