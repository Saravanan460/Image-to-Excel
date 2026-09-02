import os
import json
import base64
import requests
import logging
from config import ACTIVE_ENGINE, GEMINI_API_KEY, GEMINI_MODEL, OLLAMA_HOST, OLLAMA_MODEL

logger = logging.getLogger(__name__)

# Initialize Gemini if configured
try:
    from google import genai
    import PIL.Image
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    logger.warning("google-genai or PIL not installed. Gemini engine will not work.")



def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_data(image_path: str, system_prompt: str) -> list:
    """
    Extracts data from an image using the active engine.
    Returns a list of dictionaries (JSON objects).
    """
    logger.info(f"Using {ACTIVE_ENGINE} engine to process {os.path.basename(image_path)}")
    
    if ACTIVE_ENGINE == "gemini":
        return _extract_with_gemini(image_path, system_prompt)
    elif ACTIVE_ENGINE == "ollama":
        return _extract_with_ollama(image_path, system_prompt)
    else:
        raise ValueError(f"Unknown ACTIVE_ENGINE: {ACTIVE_ENGINE}")

def _extract_with_gemini(image_path: str, system_prompt: str) -> list:
    if not HAS_GEMINI:
        raise ImportError("google-genai is required for Gemini engine. Run: pip install google-genai pillow")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in config.")
        
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Read image using PIL for Gemini
    img = PIL.Image.open(image_path)
    
    # We pass the system prompt as instructions along with the image
    prompt = f"{system_prompt}\n\nPlease analyze the provided image and extract the data into the requested JSON format. Output ONLY valid JSON."
    
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[prompt, img]
    )
    
    return _parse_json_response(response.text)

def _extract_with_ollama(image_path: str, system_prompt: str) -> list:
    base64_image = encode_image_to_base64(image_path)
    
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": "Please analyze this image and extract the data into the requested JSON format. Output ONLY valid JSON.",
                "images": [base64_image]
            }
        ],
        "stream": False,
        "format": "json"
    }
    
    response = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload)
    response.raise_for_status()
    
    result = response.json()
    response_text = result.get("message", {}).get("content", "")
    
    return _parse_json_response(response_text)

def _parse_json_response(text: str) -> list:
    """Helper to clean up markdown and parse JSON from LLM response"""
    text = text.strip()
    
    # Remove markdown code blocks if present
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
        
    if text.endswith("```"):
        text = text[:-3]
        
    text = text.strip()
    
    try:
        data = json.loads(text)
        # Ensure it's a list (since our prompt asks for a JSON array)
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
        else:
            logger.error(f"Unexpected JSON format, expected list/dict, got {type(data)}")
            return []
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        logger.debug(f"Raw response was: {text}")
        return []
