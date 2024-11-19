from motor.motor_asyncio import AsyncIOMotorClient
import os

# Load configuration from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "translation_app")

try:
    # Create MongoDB client with a 5-second timeout
    client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DATABASE_NAME]

    # Test the connection
    client.admin.command('ping')
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None  # Prevent crashes if connection fails
