# 📄 Image to Excel Extraction Pipelines

This repository contains multiple, highly specialized data extraction pipelines designed to convert unstructured documents (like historical land surveyor cards) into perfectly structured Excel databases.

Because different types of documents require different AI approaches, this repository is split into versioned architectures:

---

## 📁 1. V2 (In Development): Multimodal Vision Pipeline
* **Recommended For:** Highly unstructured, sloppy handwriting and complex visual layouts.
* **Technology:** Direct Multimodal Vision LLMs (e.g., Gemini 1.5 Flash API or Llama 3.2 Vision).
* **Why it's better:** It reads the image contextually in a single step, completely bypassing traditional OCR typos. (This pipeline is currently being built in the root directory).

## 📁 2. V1: PaddleOCR + Local LLM Pipeline
* **Located in:** `/v1_paddleocr`
* **Recommended For:** Clean printed text, standard invoices, modern PDFs, and structured forms.
* **Technology:** PaddleOCR -> Local Qwen 2.5 7B (Ollama) -> Pydantic Validation.
* **Why it's included:** While this architecture struggled with highly messy handwriting, it is incredibly fast, 100% free, and completely offline. It is the absolute gold standard for extracting data from clean, printed documents.

---

*See the `README.md` inside each specific folder for installation and usage instructions.*
