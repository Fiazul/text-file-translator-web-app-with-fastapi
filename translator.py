import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SUPPORTED_LANGUAGES = [
    "English", "Spanish", "French", "German",
    "Italian", "Portuguese", "Dutch", "Chinese",
    "Japanese", "Korean"
]


def translate_text(text: str, target_language: str) -> str:
    if target_language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language: {target_language}. Supported languages are: {', '.join(SUPPORTED_LANGUAGES)}"
        )

    prompt = f"Translate the following text into {target_language}: {text}"

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text
