# Text File Translator Web App with FastAPI

This repository contains a web application built with FastAPI that allows users to upload text files, translate them into their desired language, and download the translated files. The application also provides a history of past translations and the option to download previous results.

---

## Features

- Upload a text file for translation.
- Translate the text file into a selected language using an API.
- Download the translated file.
- View translation history.
- Download previously translated files from the history.

---

## Setup and Installation Guide

### Prerequisites

- **Python 3.9 or above** installed on your system.
- **MongoDB Atlas** account for storing history.
- API key for translation (I got mine from https://ai.google.dev/gemini-api/docs/api-key).
- **The genai api key that google provide doesnt do directly translation. so i have write prompt for it. you can do the prompting however you want in translation.py**
---

### 1. Clone the Repository

```bash
git clone https://github.com/Fiazul/text-file-translator-web-app-with-fastapi.git
cd text-file-translator-web-app-with-fastapi

```

### 2. Install Dependencies
- It's recommended to use a virtual environment:

---

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

```

# Install the required dependencies

pip install -r requirements.txt

---


### 3. Environment Variables Setup

- Create a .env file in the root of your project and include the following variable



``` bash
MONGO_DB_URI=<MongoDB Atlas URI>
TRANSLATION_API_KEY=<API Key>

```

- MONGO_DB_URI: MongoDB Atlas URI for connecting to your database.
- TRANSLATION_API_KEY: The API key from translation provider (Google Gemini).

---


### 4. Run the Application

- To start the FastAPI application locally, use the following command

```bash
uvicorn app:app --reload
```

- The application will be accessible at: http://127.0.0.1:8000.

### Deployment on Render:

-Log in to Render.

-Create a new Web Service.

-Connect your GitHub repository.

-Set the Build Command to:

```bash

pip install -r requirements.txt

```
- Set the Start Command to:
```bash

python runserver.py
```
- Add the environment variables in the Settings tab on Render.

- Deploy the service and access it via the provided URL.

