import pandas as pd
import os
from config import EXCEL_OUTPUT, EXCEL_COLUMNS

def export_to_excel(rows: list, output_path: str = EXCEL_OUTPUT):
    if not rows:
        return
        
    df = pd.DataFrame(rows, columns=EXCEL_COLUMNS)
    
    if os.path.exists(output_path):
        # Append to existing
        existing_df = pd.read_excel(output_path)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_excel(output_path, index=False)
    else:
        # Create new
        df.to_excel(output_path, index=False)
