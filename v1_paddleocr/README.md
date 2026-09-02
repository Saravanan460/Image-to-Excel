# V1: PaddleOCR + Local LLM Pipeline

This folder contains the original V1 pipeline. It uses a two-step architecture:
1. **PaddleOCR** extracts raw text from images.
2. **Qwen 2.5 7B (via Ollama)** structures the text into JSON.
3. **Pydantic** validates the data and outputs to Excel.

## 🚀 Best Use Case
This pipeline was archived because it struggled with the highly unpredictable mistakes PaddleOCR makes on **sloppy historical handwriting**.

However, it is **highly recommended** if you are extracting data from:
* Printed receipts or invoices
* Clean, typed forms (W-2s, etc.)
* Scanned books

## 🛠️ How to Run
1. Ensure Ollama is running: `ollama serve`
2. Ensure you have the `qwen2.5:7b-instruct-q4_K_M` model downloaded.
3. Place images in `images/test_batch/`.
4. Run the pipeline:
```bash
python pipeline.py
```
5. Results will be saved in `output/results_fixed.xlsx`.
