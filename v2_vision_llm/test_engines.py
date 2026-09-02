import os
import json
import extractor
from config import SYSTEM_PROMPT_FILE

def test_engines(image_path: str):
    """
    Tests both Gemini and Ollama engines on a single image and prints the raw JSON output.
    Allows you to easily compare accuracy side-by-side.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image {image_path} not found.")
        return
        
    with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    print("="*50)
    print(f"Testing Gemini Engine on: {image_path}")
    print("="*50)
    
    # Test Gemini
    extractor.ACTIVE_ENGINE = "gemini"
    try:
        gemini_result = extractor.extract_data(image_path, system_prompt)
        print(json.dumps(gemini_result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Gemini test failed: {e}")
        
    print("\n" + "="*50)
    print(f"Testing Ollama Engine on: {image_path}")
    print("="*50)
    
    # Test Ollama
    extractor.ACTIVE_ENGINE = "ollama"
    try:
        ollama_result = extractor.extract_data(image_path, system_prompt)
        print(json.dumps(ollama_result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Ollama test failed: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test dual-engines on a single image")
    parser.add_argument("image_path", help="Path to the image to test")
    args = parser.parse_args()
    
    test_engines(args.image_path)
