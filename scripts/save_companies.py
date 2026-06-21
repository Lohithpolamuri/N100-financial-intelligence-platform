from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "raw" / "companies.xlsx"

df = pd.read_excel(file_path)

output_path = BASE_DIR / "data" / "processed" / "companies_clean.csv"

df.to_csv(output_path, index=False)

print("Saved:", output_path)
print("Rows:", len(df))