import os

# Configuration for Dual-Engine Vision Pipeline
# Choose which engine to use: "ollama" or "gemini"
ACTIVE_ENGINE = "ollama" 

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyA_T2RIx7EEfzrPJ_qCwo3mpQzAxeB1L-A") # Set your API key in environment or paste here
GEMINI_MODEL = "gemini-1.5-flash-latest"  # Using flash for high rate limits
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5vl:7b" 

# Project Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

# Shared Folders in Root Directory
IMAGE_DIR = os.path.join(ROOT_DIR, "images")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

# V2 Specific Prompts
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PROMPTS_DIR, exist_ok=True)

# System Prompt Files
SYSTEM_PROMPT_FILE = os.path.join(PROMPTS_DIR, "system_prompt.txt")
OLLAMA_SYSTEM_PROMPT_FILE = os.path.join(PROMPTS_DIR, "system_prompt_ollama.txt")

# Excel Output settings
EXCEL_OUTPUT = os.path.join(OUTPUT_DIR, "results_v5.xlsx")
ERROR_LOG = os.path.join(OUTPUT_DIR, "errors_v5.json")
PROGRESS_LOG = os.path.join(OUTPUT_DIR, "progress_v5.json")

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
