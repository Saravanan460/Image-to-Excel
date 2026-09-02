# V2 Dual-Engine Vision Pipeline

This folder contains the Version 2 implementation of the Image-to-Excel extractor, replacing the old PaddleOCR pipeline with a highly advanced **Dual-Engine Vision LLM Architecture**.

## Architecture Overview

Instead of extracting raw text via OCR and parsing it, this version sends the raw image directly to a visual language model capable of reading messy, 1960s-1980s French cursive handwriting and understanding complex document layouts.

It supports two engines:
1. **Google Gemini (Default)**: Uses the `gemini-2.5-flash` API for state-of-the-art accuracy and strict instruction following.
2. **Local Ollama**: Uses your local hardware (e.g., `llama3.2-vision` or `llava`) for 100% offline, private, and free extraction.

### Core Components

- **`config.py`**: The central configuration. Sets the `ACTIVE_ENGINE` to easily switch between Gemini and Ollama. It points to the shared `images/` and `output/` folders in the root directory.
- **`extractor.py`**: Handles all API calls. It receives the image, converts it into the proper format (Base64 for Ollama, PIL for Gemini), injects the system prompt, and returns the raw JSON array.
- **`pipeline.py`**: The main orchestration script. It iterates through all images in a target directory, extracts the JSON, validates it, and tracks progress.
- **`test_engines.py`**: A dedicated testing script that runs a single image through *both* engines sequentially, allowing for easy side-by-side accuracy comparisons.
- **`validator.py` & `export.py`**: Ports of the V1 validation logic, ensuring that dates (1957-1989), cross-multiplying lots, and strict Excel formatting remain intact.

## Setup & Usage

### 1. Engine Configuration
Open `config.py` and set your `ACTIVE_ENGINE` to `"gemini"` or `"ollama"`.

*If using Gemini:* Ensure you have installed the new SDK via `pip install google-genai` and added your API key to the config.
*If using Ollama:* Ensure the Ollama app is running in the background and you have pulled a vision model (e.g., `ollama run llama3.2-vision`).

### 2. Testing
Test a single image to ensure your engine is connected:
```bash
python test_engines.py ../images/test_batch/sample.png
```

### 3. Full Run
Run the entire pipeline on your image directory:
```bash
python pipeline.py --dir ../images/test_batch
```
Results will be saved safely to `../output/results_v2.xlsx`.
