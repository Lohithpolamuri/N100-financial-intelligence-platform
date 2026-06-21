import pandas as pd


def normalize_year(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value.startswith("Mar "):
        return value.replace("Mar ", "")

    if value.startswith("Dec "):
        return value.replace("Dec ", "")

    if value == "TTM":
        return "TTM"

    return value


def normalize_ticker(value):
    if pd.isna(value):
        return None

    return str(value).strip().upper()
print(normalize_year("Mar 2024"))
print(normalize_year("Dec 2012"))
print(normalize_year("TTM"))

print(normalize_ticker("abb"))
print(normalize_ticker(" adaniensol "))
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

df = pd.read_excel(
    DATA_DIR / "profitandloss.xlsx",
    sheet_name="Profit & Loss",
    header=1
)

df["year"] = df["year"].apply(normalize_year)
df["company_id"] = df["company_id"].apply(normalize_ticker)

print(df[["company_id", "year"]].head(10))