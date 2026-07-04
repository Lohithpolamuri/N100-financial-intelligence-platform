from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_excel(
    BASE_DIR / "data" / "raw" / "balancesheet.xlsx",
    skiprows=1
)

print(df.columns.tolist())