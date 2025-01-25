from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://cyang2023:Bthgt0SuRB39sFB1@cluster0.ka5bm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
database = client["pi-pal"]
collection = database["stats"]

fingers = 0

collection.update_one({"id": "light"}, {"$push": {"history": fingers}})