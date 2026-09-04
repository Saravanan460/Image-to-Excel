from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional, List
import re

class CardRow(BaseModel):
    No_Lot: str = ""
    Minute: str = ""
    No_Dossier: str = ""
    No_Mandat: str = ""
    Type_Travail: str = ""
    Date_Minute: str = ""
    Nom_client: str = ""
    Cadastre: str = "Saint-Jean, Ville"
    Civique_Lot: str = ""
    Rue_Lot: str = ""
    Municipalite_Lot: str = ""

    @field_validator("Rue_Lot")
    @classmethod
    def clean_rue(cls, v: str) -> str:
        # Strip 'rue ', 'carré ', 'St' to 'Saint'
        v = re.sub(r'^(rue|carré|carre)\s+', '', v, flags=re.IGNORECASE)
        v = re.sub(r'\bSt-', 'Saint-', v, flags=re.IGNORECASE)
        v = re.sub(r'\bSt\s+', 'Saint ', v, flags=re.IGNORECASE)
        return v.strip()

    # Map the JSON keys with spaces to the fields
    def __init__(self, **data):
        # Map the incoming JSON dict keys (which have spaces) to valid Python variable names
        mapped_data = {
            "No_Lot": data.get("No Lot", ""),
            "Minute": data.get("Minute", ""),
            "No_Dossier": data.get("No Dossier", ""),
            "No_Mandat": data.get("No Mandat", ""),
            "Type_Travail": data.get("Type Travail", ""),
            "Date_Minute": data.get("Date Minute", ""),
            "Nom_client": data.get("Nom client", ""),
            "Cadastre": data.get("Cadastre", "Saint-Jean, Ville"),
            "Civique_Lot": data.get("#Civique Lot", ""),
            "Rue_Lot": data.get("Rue Lot", ""),
            "Municipalite_Lot": data.get("Municipalité Lot", "")
        }
        super().__init__(**mapped_data)

    @field_validator("Minute", "No_Dossier", "No_Mandat")
    @classmethod
    def clean_minute(cls, v: str) -> str:
        return v.replace("(-1)", "").strip()

    @field_validator("Date_Minute")
    @classmethod
    def validate_date(cls, v: str) -> str:
        # Allow empty or strict YYYY-MM-DD or Unknown
        v = v.strip()
        if not v or v.lower() == "unknown":
            return "Unknown"
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            # Try to catch bad dates but let the user manually review if it fails validation later
            pass
        return v

def expand_lot_ranges(row: dict) -> List[dict]:
    lot = str(row.get("No Lot", "")).strip()
    
    # Split by "et", "&", or "," first
    parts = [p.strip() for p in re.split(r'\b(?:et|&)\b|,', lot, flags=re.IGNORECASE) if p.strip()]
    if len(parts) > 1:
        expanded_all = []
        for part in parts:
            new_row = row.copy()
            new_row["No Lot"] = part
            expanded_all.extend(expand_lot_ranges(new_row))
        return expanded_all

    
    # Pattern 1: Prefix-Start to Prefix-End (e.g. 46-35 à 46-149)
    match1 = re.search(r'^(.*?)-(\d+)\s+(?:à|a|to)\s+(.*?)-(\d+)$', lot, re.IGNORECASE)
    if match1:
        prefix1, start_num, prefix2, end_num = match1.groups()
        if prefix1 == prefix2 and int(start_num) < int(end_num):
            if int(end_num) - int(start_num) < 200:
                expanded_rows = []
                for i in range(int(start_num), int(end_num) + 1):
                    new_row = row.copy()
                    new_row["No Lot"] = f"{prefix1}-{i}"
                    expanded_rows.append(new_row)
                return expanded_rows
                
    # Pattern 2: Start to End without prefix (e.g. 106 à 114)
    match2 = re.search(r'^(\d+)\s+(?:à|a|to)\s+(\d+)$', lot, re.IGNORECASE)
    if match2:
        start_num, end_num = match2.groups()
        if int(start_num) < int(end_num):
            if int(end_num) - int(start_num) < 200:
                expanded_rows = []
                for i in range(int(start_num), int(end_num) + 1):
                    new_row = row.copy()
                    new_row["No Lot"] = str(i)
                    expanded_rows.append(new_row)
                return expanded_rows

    return [row]

def apply_ollama_business_logic(row: dict) -> List[dict]:
    new_rows = []
    
    # Rule 7: Cadastre formatting
    cadastre = str(row.get("Cadastre", ""))
    if re.search(r'Paroisse de St-Jean', cadastre, re.IGNORECASE):
        row["Cadastre"] = "Saint-Jean"
    elif re.search(r'Ville de St-Jean', cadastre, re.IGNORECASE):
        row["Cadastre"] = "Saint-Jean, Ville"
        
    # Rule 9: Civic Number & Street
    civic = str(row.get("#Civique Lot", ""))
    civic = re.sub(r'\b(et|&)\b', 'à', civic, flags=re.IGNORECASE)
    civic = re.sub(r'(\d+)\s*,\s*(\d+)', r'\1 à \2', civic)
    row["#Civique Lot"] = civic.strip()
    
    rue = str(row.get("Rue Lot", ""))
    rue = rue.replace("**", "")
    rue = re.sub(r'^(rue|carré|boul\. du)\s+', '', rue, flags=re.IGNORECASE)
    if rue.lower().startswith("de "):
        rue = rue[3:] + ", de"
    row["Rue Lot"] = rue.strip()
    
    # Rule 5: PTIE Rule
    lot = str(row.get("No Lot", ""))
    if re.search(r'\b(P\.|parties?\s+du\s+lot|pties?\s+du\s+lot|parties?|pties?)\b', lot, re.IGNORECASE):
        # Remove complex prefixes like "2 parties du lot "
        lot = re.sub(r'\b\d*\s*(parties?\s+du\s+lot|pties?\s+du\s+lot)\s*', '', lot, flags=re.IGNORECASE)
        # Remove simple prefixes like "P." or "partie"
        lot = re.sub(r'\b(P\.|parties?|pties?)\b', '', lot, flags=re.IGNORECASE).strip()
        # Clean up any leftover "du lot" just in case
        lot = re.sub(r'^du\s+lot\s+', '', lot, flags=re.IGNORECASE).strip()
        
        if not lot.upper().endswith("PTIE"):
            lot += " PTIE"
        row["No Lot"] = lot

    # Rule 4: Special Lot Expansion (-1)
    if "(-1)" in lot:
        lot_base = lot.replace("(-1)", "").strip()
        base_num = lot_base.replace(" PTIE", "").strip()
        row1 = row.copy()
        row2 = row.copy()
        row1["No Lot"] = lot_base
        row2["No Lot"] = f"{base_num}-1"
        if " PTIE" in lot_base:
            row2["No Lot"] += " PTIE"
        new_rows.extend([row1, row2])
    else:
        new_rows.append(row)
        
    return new_rows

def validate_rows(json_rows: List[dict], engine: str = "gemini") -> tuple[List[dict], bool]:
    valid_rows = []
    is_valid = True
    
    expanded_json_rows = []
    for row in json_rows:
        # We now apply the Python logic for both Gemini and Ollama
        processed_rows = apply_ollama_business_logic(row)
        for prow in processed_rows:
            expanded_json_rows.extend(expand_lot_ranges(prow))
        
    for row_dict in expanded_json_rows:
        try:
            row_obj = CardRow(**row_dict)
            
            # Enforce the strict rules programmatically
            # Date check 1957-1989
            if row_obj.Date_Minute and row_obj.Date_Minute != "Unknown":
                try:
                    year = int(row_obj.Date_Minute[:4])
                    if year > 1989 or year < 1957:
                        # Should have been skipped, skip it now
                        continue
                except ValueError:
                    pass

            # Convert back to standard dict
            valid_rows.append({
                "No Lot": row_obj.No_Lot,
                "Minute": row_obj.Minute,
                "No Dossier": row_obj.No_Dossier,
                "No Mandat": row_obj.No_Mandat,
                "Type Travail": row_obj.Type_Travail,
                "Date Minute": row_obj.Date_Minute,
                "Nom client": row_obj.Nom_client,
                "Cadastre": row_obj.Cadastre,
                "#Civique Lot": row_obj.Civique_Lot,
                "Rue Lot": row_obj.Rue_Lot,
                "Municipalité Lot": row_obj.Municipalite_Lot
            })
        except ValidationError as e:
            print(f"Validation error: {e}")
            is_valid = False
            
    return valid_rows, is_valid
