# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# import os

# uri = os.getenv("MONGO_DB_URI")

# client = MongoClient(uri, server_api=ServerApi('1'))

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client['translation_db']  # Connect to your MongoDB database
collection = db['translations']  # Use the correct collection name

# Test by inserting a test document
collection.insert_one({"test": "MongoDB is working!"})

# Retrieve and print the document
result = collection.find_one({"test": "MongoDB is working!"})
print(result)
