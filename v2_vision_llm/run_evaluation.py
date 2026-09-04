import os
import glob
import json
from PIL import Image
from extractor import extract_data

with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

test_dir = os.path.join("..", "images", "test_batch")
image_files = glob.glob(os.path.join(test_dir, "*.png"))

results = {}

for img_path in image_files:
    if "_cropped" in img_path:
        continue
    print(f"Testing {os.path.basename(img_path)}...")
    try:
        # We need to crop out the table from the screenshot to prevent the AI from cheating
        img = Image.open(img_path)
        width, height = img.size
        # Crop the top 65% of the image (the card itself)
        cropped = img.crop((0, 0, width, int(height * 0.65)))
        cropped_path = img_path.replace(".png", "_cropped.png")
        cropped.save(cropped_path)
        
        # Process with the LLM
        json_res = extract_data(cropped_path, system_prompt)
        results[os.path.basename(img_path)] = json_res
        
        # Clean up
        os.remove(cropped_path)
    except Exception as e:
        print(f"Error on {img_path}: {e}")

# Save results to a markdown file
with open("evaluation_results.md", "w", encoding="utf-8") as f:
    f.write("# Full Evaluation of PDF Rules against Gemini 2.5 Flash\n\n")
    for name, res in results.items():
        f.write(f"## {name}\n")
        f.write(f"```json\n{json.dumps(res, indent=2, ensure_ascii=False)}\n```\n\n")

print("Evaluation finished! Check evaluation_results.md")
