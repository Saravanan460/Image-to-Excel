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

def validate_rows(json_rows: List[dict]) -> tuple[List[dict], bool]:
    valid_rows = []
    is_valid = True
    
    expanded_json_rows = []
    for row in json_rows:
        expanded_json_rows.extend(expand_lot_ranges(row))
        
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
