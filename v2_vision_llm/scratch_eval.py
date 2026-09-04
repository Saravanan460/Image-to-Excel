import os
import json
import extractor
from config import OLLAMA_SYSTEM_PROMPT_FILE
from validator import validate_rows

image_dir = "../images/test_batch"
images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.png') or f.endswith('.jpg')]

results = {}

with open(OLLAMA_SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
    prompt = f.read()

extractor.ACTIVE_ENGINE = "ollama"

for img in images:
    results[img] = {}
    print(f"Processing {img}...")
    
    try:
        raw_ollama, raw_text = extractor.extract_data(img, prompt)
        validated_ollama, _ = validate_rows(raw_ollama, engine="ollama")
        results[img]["ollama"] = {"raw": raw_ollama, "validated": validated_ollama, "llm_text": raw_text}
    except Exception as e:
        results[img]["ollama"] = {"error": str(e)}

with open("scratch_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("Evaluation complete.")
