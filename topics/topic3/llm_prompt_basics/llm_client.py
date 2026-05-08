"""LLM client helpers for Topic 3."""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def get_client() -> genai.Client:
    """Create a Gemini client from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in environment variables.")
    if api_key == "your_gemini_api_key_here":
        raise ValueError("Please replace placeholder GEMINI_API_KEY in .env.")
    return genai.Client(api_key=api_key)


def get_model_name() -> str:
    """Return configured model name with a safe default."""
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
