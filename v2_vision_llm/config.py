import os

# Configuration for Dual-Engine Vision Pipeline
# Choose which engine to use: "ollama" or "gemini"
ACTIVE_ENGINE = "gemini" 

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyA_T2RIx7EEfzrPJ_qCwo3mpQzAxeB1L-A") # Set your API key in environment or paste here
GEMINI_MODEL = "gemini-2.5-flash"

# Ollama Configuration
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2-vision" # If you get 'mllama' error, you can change this to "llava"

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

# System Prompt File
SYSTEM_PROMPT_FILE = os.path.join(PROMPTS_DIR, "system_prompt.txt")

# Excel Output settings
EXCEL_OUTPUT = os.path.join(OUTPUT_DIR, "results_v2.xlsx")
ERROR_LOG = os.path.join(OUTPUT_DIR, "errors_v2.json")
PROGRESS_LOG = os.path.join(OUTPUT_DIR, "progress_v2.json")

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
