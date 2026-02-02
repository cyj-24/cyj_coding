import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def list_gemini_models():
    print("[*] Listing available Gemini models...")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model Name: {m.name}, Display Name: {m.display_name}")
    except Exception as e:
        print(f"[!] Error listing models: {e}")

if __name__ == "__main__":
    list_gemini_models()
