import os
import time
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from dotenv import load_dotenv
from main import app
import uvicorn
import asyncio
load_dotenv()


MONGO_URI = os.getenv("MONGO_DB_URI")
DATABASE_NAME = "translation_app"


async def connect_to_mongo():

    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DATABASE_NAME]
        print("Connected to MongoDB successfully.")
        return db
    except Exception as e:
        print(f"Error during MongoDB connection: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
        return await connect_to_mongo()


@app.on_event("startup")
async def startup_event():
    """This function runs when the FastAPI app starts."""
    print("Starting FastAPI server...")
    db = await connect_to_mongo()
    print("MongoDB connection established")

if __name__ == "__main__":
    print("Running server with uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
