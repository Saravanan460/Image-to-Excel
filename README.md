# 📄 Image to Excel: Specialized OCR Extraction Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PaddleOCR](https://img.shields.io/badge/PaddleOCR-Powered-orange)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black)

A highly specialized data extraction pipeline designed to convert unstructured, historical handwritten land surveyor index cards (Laurent Veronneau) into a perfectly structured Excel database.

---

## ⚙️ How It Works (The Workflow)

This pipeline operates on a robust **Two-Step Architecture (OCR + AI)**, allowing it to remain completely offline and free.

1. 🔍 **Text Extraction (PaddleOCR)**  
   Scans raw `.jpg` or `.png` images and extracts all detectable text strings.
2. 🧠 **Contextual Structuring (Qwen 2.5 7B via Ollama)**  
   The raw OCR text is passed to a local Large Language Model. Using advanced prompt engineering, the LLM applies rigid business logic (e.g., cross-multiplying lot numbers, skipping dates >= 1990, deducing address locations).
3. 🛡️ **Validation (Pydantic)**  
   Python strictly validates the LLM's JSON output, enforcing correct date formats (`YYYY-MM-DD`), expanding address ranges, and dropping invalid records.
4. 📊 **Excel Export (Pandas)**  
   The clean, structured JSON is flattened into discrete rows and exported to `results_fixed.xlsx`.

---

## 🐛 Challenges & Flaws Encountered

The biggest challenge in this architecture was **PaddleOCR's unpredictable garbled outputs** on messy handwriting.

* **The Problem:** The business logic required strict rules (e.g., Date > 1957). However, PaddleOCR would randomly hallucinate characters or merge words due to faded ink (e.g., extracting `18-03-76` as `1e18-03-76`, or merging `SUBDIVISION P.63-223`).
* **The Collision:** Applying strict Python logic to stochastic OCR errors caused the pipeline to crash or skip valid data.
* **The Fix:** We shifted the heavy lifting to the LLM. By explicitly teaching the LLM how to identify and *deduce* PaddleOCR's specific brand of typos, the LLM was able to reconstruct the correct text contextually before Python validated it.

---

## 🚀 Future Roadmap: Moving to Vision AI

While the current two-step process is functional, OCR mistakes are fundamentally unpredictable. 

**Our next step is to abandon PaddleOCR entirely and upgrade to a Direct Multimodal Vision LLM** (such as `Llama 3.2 Vision` locally, or `Gemini 1.5 Flash` via API). 

By passing the raw image directly to a Vision AI, the model can read the handwriting visually in a single step—bypassing OCR typos completely and achieving near 100% accuracy on highly unstructured historical documents.

---

## 💡 Alternative Uses For This Repo

While historical handwriting pushed this specific OCR architecture to its limits, the `PaddleOCR -> Local LLM -> Pydantic` workflow is **absolutely stellar** for other use cases. 

This repository can be easily modified and is highly recommended for:

| Use Case | Why It Works Well Here |
| :--- | :--- |
| **🧾 Printed Invoices & Receipts** | PaddleOCR reads standard printed fonts flawlessly, and the LLM easily maps the clean text to JSON. |
| **📋 Modern Structured Forms** | Perfect for W-2s, tax forms, or digital PDFs where layout is consistent. |
| **📚 Data Mining Printed Books** | Excellent at extracting structured tables or paragraphs from clean, printed book scans. |

If you are dealing with clean, printed text, this architecture provides an incredibly fast, 100% free, and completely offline data extraction engine!
