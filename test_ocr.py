import os
from ocr_engine import OCREngine

ocr = OCREngine()
for f in os.listdir('images/test_batch'):
    if f.endswith('.jpg') or f.endswith('.png'):
        print(f"\n--- {f} ---")
        print(ocr.extract_text(os.path.join('images/test_batch', f)))
