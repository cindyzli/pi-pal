import os
from pymongo import MongoClient
from llama_index.core import VectorStoreIndex, Document 

os.environ["OPENAI_API_KEY"] = "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"

uri = "mongodb+srv://cyang2023:Bthgt0SuRB39sFB1@cluster0.ka5bm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
database = client["pi-pal"]
collection = database["stats1"]

documents = collection.find({}, {"action": "call_sign"}).limit(3)

document_list = []
for doc in documents:
    text_content = f"Action: {doc.get('action', 'Unknown')}, Value: {doc.get('value', 'Unknown')}, Timestamp: {doc.get('timestamp', 'Unknown')}"
    document_list.append(Document(text=text_content))  #

document_list = document_list[:3]
index = VectorStoreIndex.from_documents(document_list)


query = "What data should be concerning about user actions?"
response = index.query(query)

print(response)
