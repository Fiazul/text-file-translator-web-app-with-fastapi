from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse, JSONResponse
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
from translator import translate_text
import asyncio
import os
import uuid
from pymongo import MongoClient
from datetime import datetime, timezone
from serializers import serialize_object
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["translation_service"]
history_collection = db["file_history"]


class TranslationHistory(BaseModel):
    sessionId: str
    fileProcessed: dict


class TranslationRequest(BaseModel):
    text: str
    target_language: str


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.post("/translate_text/")
async def translate_text_endpoint(request: TranslationRequest):
    try:
        translated_text = translate_text(request.text, request.target_language)
        return JSONResponse(content={"translated_text": translated_text})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/translate_file/")
async def translate_file_endpoint(target_language: Annotated[str, Form()], file: Annotated[UploadFile, File()]):
    if file is None:
        raise HTTPException(
            status_code=400, detail="No file provided. Please upload a file."
        )

    if not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400, detail="Only .txt files are supported."
        )

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    content = await file.read()

    file_path = f"uploads/{uuid.uuid4().hex}.txt"
    try:
        with open(file_path, "w", encoding="utf-8") as buffer:
            buffer.write(content.decode("utf-8"))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving file: {str(e)}"
        )

    try:
        translated_file_name = f"translated_{uuid.uuid4().hex}.txt"
        translated_text = translate_text(content, target_language)
        translated_file_path = f"outputs/{translated_file_name}"

        with open(translated_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(translated_text)

        history_collection.insert_one({
            "sessionId": str(uuid.uuid4()),
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "fileProcessed": {
                "fileName": file.filename,
                "filePath": translated_file_path,
                "processedAt": datetime.now(timezone.utc).isoformat(),
                "TranslatedFilename": translated_file_name,
                "result": "Success"
            }
        })

        return JSONResponse(
            content={
                "message": "Translation successful",
                "translated_file_path": translated_file_path,
                "translated_file_name": translated_file_name,
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error during translation: {str(e)}"
        )


@app.get("/download_translated_file/")
async def download_translated_file(file_name: str):
    file_path = os.path.join("outputs", file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_text()
            if message == "start_translation":
                await websocket.send_text("File received, starting translation...")

                await websocket.send_text("Translating...")
                await asyncio.sleep(3)

                await websocket.send_text("Translation complete! Saving file...")
                await asyncio.sleep(2)

                await websocket.send_text("Translation complete. You can download your file.")
            else:
                await websocket.send_text(f"Unknown command: {message}")
    except WebSocketDisconnect:
        print("Client disconnected")


@app.get("/history/")
async def get_translation_history():
    try:
        # Fetch history from MongoDB
        history = list(history_collection.find())

        # Serialize the documents
        serialized_history = [serialize_object(record) for record in history]

        return JSONResponse(content={"history": serialized_history})

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching history: {str(e)}")
