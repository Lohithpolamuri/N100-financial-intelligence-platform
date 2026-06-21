import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"

PROCESSED_DIR.mkdir(exist_ok=True)

df = pd.read_excel(
    RAW_DIR / "profitandloss.xlsx",
    sheet_name="Profit & Loss",
    header=1
)

df.to_csv(
    PROCESSED_DIR / "profitandloss_clean.csv",
    index=False
)

print("Saved successfully!")