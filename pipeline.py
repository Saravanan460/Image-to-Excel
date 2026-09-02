import os
import json
from tqdm import tqdm
from config import IMAGE_DIR, TEST_BATCH_DIR, EXCEL_OUTPUT, ERROR_LOG, PROGRESS_LOG
from ocr_engine import OCREngine
from llm_extractor import LLMExtractor
from validator import validate_rows
from export import export_to_excel

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

def run_pipeline(directory=TEST_BATCH_DIR):
    print("Starting pipeline initialization...")
    ocr_engine = OCREngine()
    llm = LLMExtractor()
    
    processed_files = load_progress()
    
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    remaining_files = [f for f in image_files if f not in processed_files]
    
    print(f"Found {len(image_files)} total images. {len(remaining_files)} remaining to process.")
    
    for filename in tqdm(remaining_files, desc="Processing Images"):
        image_path = os.path.join(directory, filename)
        
        # 1. OCR
        ocr_text = ocr_engine.extract_text(image_path)
        if not ocr_text:
            log_error(filename, "No text extracted by OCR.")
            continue
            
        # 2. LLM Extraction
        raw_json_rows = llm.extract_data(ocr_text)
        if not raw_json_rows:
            log_error(filename, "LLM failed to return valid JSON.")
            continue
            
        # 3. Validation & Business Logic
        valid_rows, is_valid = validate_rows(raw_json_rows)
        if not is_valid or not valid_rows:
            log_error(filename, "Row validation failed or all rows were skipped (e.g. >1989 dates).")
            # We still might want to save valid rows if some failed but some succeeded. 
            # In this implementation, valid_rows contains what succeeded.
            
        # 4. Export
        if valid_rows:
            export_to_excel(valid_rows)
            
        # 5. Save Progress
        processed_files.add(filename)
        save_progress(processed_files)
        
    print(f"Pipeline finished! Results saved to {EXCEL_OUTPUT}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action='store_true', help='Run on the entire images directory instead of test_batch')
    args = parser.parse_args()
    
    target_dir = IMAGE_DIR if args.full else TEST_BATCH_DIR
    run_pipeline(target_dir)
