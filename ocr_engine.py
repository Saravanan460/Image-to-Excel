import logging
import ssl
import certifi

# Monkey-patch SSL to use certifi instead of Windows certificate store
# This prevents the "ssl.SSLError: [ASN1: NOT_ENOUGH_DATA]" crash on import
_orig_create_default_context = ssl.create_default_context

def _patched_create_default_context(purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None):
    if cafile is None and capath is None and cadata is None:
        cafile = certifi.where()
    return _orig_create_default_context(purpose=purpose, cafile=cafile, capath=capath, cadata=cadata)

ssl.create_default_context = _patched_create_default_context

from paddleocr import PaddleOCR

logging.getLogger('ppocr').setLevel(logging.ERROR) # Suppress noisy paddleocr logs

class OCREngine:
    def __init__(self):
        print("Initializing PaddleOCR (this may take a moment on first run)...")
        # use_angle_cls=True to automatically detect and rotate images if needed
        # lang='fr' for French language
        self.ocr = PaddleOCR(use_angle_cls=True, lang='fr')
        print("PaddleOCR Initialized.")

    def extract_text(self, image_path: str) -> str:
        """
        Extracts text from an image preserving spatial layout.
        Returns text with position hints so the LLM can understand
        what's at the top-left (Minute number), what's a date, etc.
        """
        result = self.ocr.ocr(image_path, cls=True)
        
        if not result or not result[0]:
            return ""
            
        lines = result[0]
        
        # Sort by Y position (top to bottom), then X (left to right)
        sorted_lines = sorted(lines, key=lambda l: (int(l[0][0][1]), int(l[0][0][0])))
        
        # Group into visual rows by Y-proximity (within 15px = same row)
        visual_rows = []
        current_row = []
        current_y = -100
        
        for line in sorted_lines:
            box = line[0]
            text = line[1][0]
            score = line[1][1]
            y_pos = int(box[0][1])
            x_pos = int(box[0][0])
            
            if abs(y_pos - current_y) > 15:
                # New visual row
                if current_row:
                    visual_rows.append(current_row)
                current_row = [(x_pos, y_pos, text, score)]
                current_y = y_pos
            else:
                current_row.append((x_pos, y_pos, text, score))
        
        if current_row:
            visual_rows.append(current_row)
        
        # Format with layout awareness
        output_lines = []
        for i, row in enumerate(visual_rows):
            # Sort items in each visual row by X position (left to right)
            row.sort(key=lambda item: item[0])
            
            if i == 0:
                # First row: the top-left number is almost always the Minute number
                texts = [item[2] for item in row]
                # Mark the first element as the top-left number
                if texts:
                    output_lines.append(f"[TOP-LEFT NUMBER: {texts[0]}]  {'  '.join(texts[1:])}")
                continue
            
            # For other rows, join with spacing to indicate layout
            texts = [item[2] for item in row]
            output_lines.append("  ".join(texts))
        
        return "\n".join(output_lines)

if __name__ == "__main__":
    engine = OCREngine()
