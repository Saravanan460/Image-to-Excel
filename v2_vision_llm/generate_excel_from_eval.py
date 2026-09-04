import json
import re
from export import export_to_excel
from validator import validate_rows

# Read the evaluation results
with open("evaluation_results.md", "r", encoding="utf-8") as f:
    content = f.read()

# Extract all JSON blocks
json_blocks = re.findall(r"```json\n(.*?)\n```", content, re.DOTALL)

all_valid_rows = []

for block in json_blocks:
    try:
        rows = json.loads(block)
        valid_rows, is_valid = validate_rows(rows)
        if is_valid and valid_rows:
            all_valid_rows.extend(valid_rows)
    except Exception as e:
        print(f"Error parsing block: {e}")

if all_valid_rows:
    export_to_excel(all_valid_rows)
    print(f"Successfully exported {len(all_valid_rows)} rows to Excel from the evaluation cache!")
else:
    print("No valid rows found.")
