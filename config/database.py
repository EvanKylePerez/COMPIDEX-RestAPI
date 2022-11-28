from pymongo import MongoClient


client = MongoClient("mongodb+srv://admin:dbAqYlsDTuB93Zu8@compidexdbserver.gxyl71x.mongodb.net/?retryWrites=true&w=majority")
db = client.compidex_application

collection_name = db["compidex_app"]
