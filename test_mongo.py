from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://cyang2023:Bthgt0SuRB39sFB1@cluster0.ka5bm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
database = client["pi-pal"]
collection = database["stats1"]

entries = [
    {"action": "call_sign", "value": "Passive", "timestamp": "2025-01-25 10:00:00"},  
    {"action": "dimming_lights", "value": "50%", "timestamp": "2025-01-25 10:05:00"},  
    {"action": "nurse_request", "value": "Pain killers", "timestamp": "2025-01-25 10:10:00"},  
    {"action": "call_sign", "value": "Emergency", "timestamp": "2025-01-25 10:15:00"},  
    {"action": "dimming_lights", "value": "75%", "timestamp": "2025-01-25 10:20:00"},  
]

for entry in entries:
    # Insert each entry as a separate document
    collection.insert_one(entry)

# Fetch and print the documents to verify
documents = collection.find()
for document in documents:
    print(document)
