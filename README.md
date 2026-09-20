# 📄 Image to Excel Extraction Pipelines

This repository contains multiple, highly specialized data extraction pipelines designed to convert unstructured documents (like historical land surveyor cards) into perfectly structured Excel databases.

Because different types of documents require different AI approaches, this repository is split into versioned architectures:

---

## 🚀 1. V2 (In Development): Multimodal Vision Pipeline
* **Located in:** `/v2_vision_llm`
* **Recommended For:** Highly unstructured, sloppy handwriting and complex visual layouts.
* **Technology:** Direct Multimodal Vision LLMs (e.g., Gemini 1.5 Flash API or Qwen Vision via Ollama) + Pydantic Validation + Advanced Python Business Logic.
* **Key Features:** Includes an evaluation framework for testing different LLM engines, automatic lot range expansion, and specialized address/cadastre formatting rules.
* **Why it's better:** It reads the image contextually in a single step, completely bypassing traditional OCR typos.

## 📁 2. V1: PaddleOCR + Local LLM Pipeline
* **Located in:** `/v1_paddleocr`
* **Recommended For:** Clean printed text, standard invoices, modern PDFs, and structured forms.
* **Technology:** PaddleOCR -> Local Qwen 2.5 7B (Ollama) -> Pydantic Validation.
* **Why it's included:** While this architecture struggled with highly messy handwriting, it is incredibly fast, 100% free, and completely offline. It is the absolute gold standard for extracting data from clean, printed documents.

---

*See the `README.md` inside each specific folder for installation and usage instructions.*

---

## 🛠️ How It Works: Image to Rows

The V2 pipeline uses Vision LLMs to contextually read unstructured cards and map them to a strict JSON structure. This output is then processed by advanced Python business logic to handle edge cases and Cartesian products (such as expanding lot ranges).

### Example 1: Clean Extraction
Here is a typical surveyor card:

![Clean Example](images/Screenshot%202026-09-02%20080416.png)

**Raw JSON Output (from Vision LLM):**
```json
[
  {
    "Minute": "10882",
    "No Dossier": "10882",
    "No Mandat": "10882",
    "No Lot": "46",
    "Date Minute": "1979-02-12",
    "Nom client": "John Doe",
    "Cadastre": "Saint-Jean"
  }
]
```

**Final Excel Row:**
| Minute | No Dossier | No Lot | Date Minute | Nom client | Cadastre |
|--------|------------|--------|-------------|------------|----------|
| 10882  | 10882      | 46     | 1979-02-12  | John Doe   | Saint-Jean|

### Example 2: Edge Cases & Cartesian Product (Lot Expansion)
When a card contains a range of lots, the Vision LLM extracts the literal text. Our validation script then performs a **Cartesian Product expansion**, turning that single extracted object into individual Excel rows so the database is highly structured and searchable.

![Edge Case Example](images/test_batch/Screenshot%202026-09-01%20183147.png)

**Raw JSON Output (from Vision LLM):**
```json
[
  {
    "Minute": "12345",
    "No Lot": "46-35 à 46-37",
    "Type Travail": "Certificat de localisation"
  }
]
```

**Final Excel Rows (Automatically Expanded):**
| Minute | No Lot | Type Travail |
|--------|--------|--------------|
| 12345  | 46-35  | Certificat de localisation |
| 12345  | 46-36  | Certificat de localisation |
| 12345  | 46-37  | Certificat de localisation |

**Other Handled Edge Cases:**
- **Comma & Ampersand Expansion:** `Lot 123 & 124` becomes two rows.
- **Suffix Expansion:** `10882(-1)` expands to two rows: `10882` and `10882-1`.
- **PTIE Formatting:** Automatically cleans prefixes and appends `PTIE` to lots if required.
