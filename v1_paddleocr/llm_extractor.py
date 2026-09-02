import requests
import json
import os
from config import OLLAMA_HOST, MODEL_NAME, PROMPTS_DIR

class LLMExtractor:
    def __init__(self):
        with open(os.path.join(PROMPTS_DIR, "system_prompt.txt"), "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
            
    def extract_data(self, ocr_text: str) -> list:
        if not ocr_text.strip():
            return []
            
        url = f"{OLLAMA_HOST}/api/chat"
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Extract the data from this OCR text:\n\n{ocr_text}"}
            ],
            "stream": False,
            "options": {
                "temperature": 0.0 # Deterministic
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            result_text = response.json().get("message", {}).get("content", "")
            
            # Clean up the markdown JSON if ollama returns it
            result_text = result_text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
                
            return json.loads(result_text.strip())
            
        except requests.exceptions.RequestException as e:
            print(f"Ollama API Error: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from LLM: {result_text}")
            return []

if __name__ == "__main__":
    extractor = LLMExtractor()
    # print(extractor.extract_data("Test OCR Text"))
