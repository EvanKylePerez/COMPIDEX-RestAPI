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