import os

# Project Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PROMPTS_DIR, exist_ok=True)

# File Paths
TEST_BATCH_DIR = os.path.join(IMAGE_DIR, "test_batch")
os.makedirs(TEST_BATCH_DIR, exist_ok=True)

EXCEL_OUTPUT = os.path.join(OUTPUT_DIR, "results_fixed.xlsx")
ERROR_LOG = os.path.join(OUTPUT_DIR, "errors.json")
PROGRESS_LOG = os.path.join(OUTPUT_DIR, "progress.json")

# LLM Config
OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "qwen2.5:7b-instruct-q4_K_M"

# Excel Columns
EXCEL_COLUMNS = [
    "No Lot",
    "Minute",
    "No Dossier",
    "No Mandat",
    "Type Travail",
    "Date Minute",
    "Nom client",
    "Cadastre",
    "#Civique Lot",
    "Rue Lot",
    "Municipalité Lot"
]
