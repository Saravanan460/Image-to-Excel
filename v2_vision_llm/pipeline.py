import os
import json
from tqdm import tqdm
from config import IMAGE_DIR, EXCEL_OUTPUT, ERROR_LOG, PROGRESS_LOG, SYSTEM_PROMPT_FILE
from extractor import extract_data
from validator import validate_rows
from export import export_to_excel
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_progress():
    if os.path.exists(PROGRESS_LOG):
        with open(PROGRESS_LOG, 'r') as f:
            return set(json.load(f))
    return set()

def save_progress(processed_files):
    with open(PROGRESS_LOG, 'w') as f:
        json.dump(list(processed_files), f)

def log_error(filename, reason):
    errors = {}
    if os.path.exists(ERROR_LOG):
        with open(ERROR_LOG, 'r') as f:
            errors = json.load(f)
    errors[filename] = reason
    with open(ERROR_LOG, 'w') as f:
        json.dump(errors, f, indent=4)

def run_pipeline(directory=IMAGE_DIR):
    logger.info("Starting Vision LLM pipeline initialization...")
    
    with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    processed_files = load_progress()
    
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    remaining_files = [f for f in image_files if f not in processed_files]
    
    logger.info(f"Found {len(image_files)} total images. {len(remaining_files)} remaining to process.")
    
    for filename in tqdm(remaining_files, desc="Processing Images"):
        image_path = os.path.join(directory, filename)
        
        # 1. Vision LLM Extraction
        try:
            raw_json_rows = extract_data(image_path, system_prompt)
        except Exception as e:
            logger.error(f"Extraction failed for {filename}: {e}")
            log_error(filename, f"Extraction Exception: {str(e)}")
            continue
            
        if not raw_json_rows:
            log_error(filename, "Vision LLM failed to return valid JSON.")
            continue
            
        # 2. Validation & Business Logic
        valid_rows, is_valid = validate_rows(raw_json_rows)
        if not is_valid or not valid_rows:
            log_error(filename, "Row validation failed or all rows were skipped (e.g. >1989 dates).")
            
        # 3. Export
        if valid_rows:
            export_to_excel(valid_rows)
            
        # 4. Save Progress
        processed_files.add(filename)
        save_progress(processed_files)
        
    logger.info(f"Pipeline finished! Results saved to {EXCEL_OUTPUT}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, help='Specific directory to process', default=IMAGE_DIR)
    args = parser.parse_args()
    
    run_pipeline(args.dir)
