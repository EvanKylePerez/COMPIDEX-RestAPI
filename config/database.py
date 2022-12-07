from pymongo import MongoClient


client = MongoClient("mongodb+srv://admin:dbAqYlsDTuB93Zu8@compidexdbserver.gxyl71x.mongodb.net/?retryWrites=true&w=majority")
db = client.compidex_application

merchants_data = db["compidex_merchants"]
products_data = db["compidex_products"]
users_data = db["compidex_users"]
