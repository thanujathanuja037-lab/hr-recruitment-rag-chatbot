
"""Check that the Gemini API key works and list accessible models."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key or api_key == "paste_your_key_here":
    raise SystemExit(
        "GOOGLE_API_KEY is missing. Check your .env file."
    )

url = "https://generativelanguage.googleapis.com/v1beta/models"

try:
    response = requests.get(
        url,
        params={"key": api_key},
        timeout=30,
    )

    if response.status_code != 200:
        raise SystemExit(
            f"Gemini API check failed ({response.status_code}). "
            "Check your API key, API access, and quota."
        )

    models = response.json().get("models", [])

    if not models:
        raise SystemExit("API responded, but no models were listed.")

    print("Gemini API connection: OK")
    print("\nAvailable models:")

    for model in models:
        name = model.get("name", "")
        methods = model.get("supportedGenerationMethods", [])
        print(f"- {name} | methods: {', '.join(methods)}")

except requests.RequestException as e:
    raise SystemExit(f"Network error while checking Gemini API: {e}")
