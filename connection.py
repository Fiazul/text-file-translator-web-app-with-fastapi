from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "MONGO_DB_URI"
DATABASE_NAME = "translation_app"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
