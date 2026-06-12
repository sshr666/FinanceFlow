import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SARVAM_URL = "https://api.sarvam.ai/v1/translate"
TIMEOUT = 30

# Sarvam uses source_language_code / target_language_code format
LANG_MAP = {
    "hi": {"source": "en-IN", "target": "hi-IN"},
    "te": {"source": "en-IN", "target": "te-IN"},
}


def get_api_key():
    try:
        import streamlit as st
        key = st.secrets.get("SARVAM_API_KEY")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("SARVAM_API_KEY")


def translate(text, target_language):
    if not text or not text.strip():
        return None, "No text provided for translation."
    if target_language not in LANG_MAP:
        return None, f"Unsupported target language: {target_language}"

    api_key = get_api_key()
    if not api_key:
        return None, "SARVAM_API_KEY not configured. Set it in .env or Streamlit secrets."

    lang_codes = LANG_MAP[target_language]

    try:
        response = requests.post(
            SARVAM_URL,
            headers={
                "API-Subscription-Key": api_key,
                "Content-Type": "application/json",
            },
            json={
                "input": text,
                "source_language_code": lang_codes["source"],
                "target_language_code": lang_codes["target"],
            },
            timeout=TIMEOUT,
        )
        result = response.json()
        if "error" in result:
            return None, f"Sarvam error: {result['error']}"
        response.raise_for_status()
        translated = result.get("translated_text", "").strip()
        if not translated:
            return None, "Sarvam returned an empty translation."
        return translated, None
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to Sarvam AI API."
    except requests.exceptions.Timeout:
        return None, "Sarvam AI request timed out."
    except requests.exceptions.RequestException as e:
        return None, f"Sarvam AI request failed: {e}"
    except (json.JSONDecodeError, KeyError) as e:
        return None, f"Failed to parse Sarvam response: {e}"
