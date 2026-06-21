from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

excel_files = list(DATA_DIR.glob("*.xlsx"))

if not excel_files:
    print("No Excel files found in data/raw/")
else:
    print(f"Found {len(excel_files)} Excel files")

    for file in excel_files:
        print("\n" + "=" * 50)
        print("FILE:", file.name)

        try:
            xl = pd.ExcelFile(file)

            print("Sheets:", xl.sheet_names)

            for sheet in xl.sheet_names:
                df = pd.read_excel(file, sheet_name=sheet)

                print(f"\nSheet: {sheet}")
                print("Rows:", df.shape[0])
                print("Columns:", df.shape[1])
                print("Column Names:")
                print(df.columns.tolist())

                break

        except Exception as e:
            print("Error:", e)