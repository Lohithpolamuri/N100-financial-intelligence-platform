from pathlib import Path
import pandas as pd

# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Read cleaned file
df = pd.read_csv(BASE_DIR / "data" / "processed" / "profitandloss_clean.csv")

failures = []

# DQ-01: company_id should not be null
null_company = df[df["company_id"].isnull()]

for index in null_company.index:
    failures.append([index, "DQ-01", "company_id is NULL"])

# DQ-02: year should not be null
null_year = df[df["year"].isnull()]

for index in null_year.index:
    failures.append([index, "DQ-02", "year is NULL"])

# DQ-03: sales should not be negative
negative_sales = df[df["sales"] < 0]

for index in negative_sales.index:
    failures.append([index, "DQ-03", "sales is negative"])

# Create failures dataframe
failure_df = pd.DataFrame(
    failures,
    columns=["row_number", "rule_id", "issue"]
)

# Save output file
output_path = BASE_DIR / "output" / "validation_failures.csv"

failure_df.to_csv(output_path, index=False)

print("=" * 50)
print("VALIDATION COMPLETE")
print("=" * 50)
print("Total Records :", len(df))
print("Failures Found:", len(failure_df))
print("Output File   :", output_path)
# DQ-04: expenses should not be negative
negative_expenses = df[df["expenses"] < 0]

for index in negative_expenses.index:
    failures.append([index, "DQ-04", "expenses is negative"])
    # DQ-05: net_profit should not be null
    null_profit = df[df["net_profit"].isnull()]

    for index in null_profit.index:
        failures.append([index, "DQ-05", "net_profit is NULL"])
        # DQ-06: company_id should not be empty
        empty_company = df[df["company_id"].astype(str).str.strip() == ""]

        for index in empty_company.index:
            failures.append([index, "DQ-06", "company_id is empty"])
            # DQ-07: year should not be empty
            empty_year = df[df["year"].astype(str).str.strip() == ""]

            for index in empty_year.index:
                failures.append([index, "DQ-07", "year is empty"])
                # DQ-08: sales should not be null
                null_sales = df[df["sales"].isnull()]

                for index in null_sales.index:
                    failures.append([index, "DQ-08", "sales is NULL"])
                    # DQ-09: operating_profit should not be null
                    null_op = df[df["operating_profit"].isnull()]

                    for index in null_op.index:
                        failures.append([index, "DQ-09", "operating_profit is NULL"])
                        # DQ-10: expenses should not be NULL
                        null_expenses = df[df["expenses"].isnull()]

                        for index in null_expenses.index:
                            failures.append([index, "DQ-10", "expenses is NULL"])
                            # DQ-11: net_profit should not be negative
                            negative_profit = df[df["net_profit"] < 0]

                            for index in negative_profit.index:
                                failures.append([index, "DQ-11", "net_profit is negative"])
                                # DQ-12: operating_profit should not be negative
                                negative_op = df[df["operating_profit"] < 0]

                                for index in negative_op.index:
                                    failures.append([index, "DQ-12", "operating_profit is negative"])
                                    # DQ-13: company_id length should be > 0
                                    invalid_company = df[df["company_id"].astype(str).str.len() == 0]

                                    for index in invalid_company.index:
                                        failures.append([index, "DQ-13", "invalid company_id"])
                                        # DQ-14: year length should be > 0
                                        invalid_year = df[df["year"].astype(str).str.len() == 0]

                                        for index in invalid_year.index:
                                            failures.append([index, "DQ-14", "invalid year"])
                                            # DQ-15: sales should be greater than expenses
                                            invalid_margin = df[df["sales"] < df["expenses"]]

                                            for index in invalid_margin.index:
                                                failures.append([index, "DQ-15", "sales less than expenses"])
                                                # DQ-16: duplicate company-year combinations
                                                duplicates = df[
                                                    df.duplicated(subset=["company_id", "year"], keep=False)]

                                                for index in duplicates.index:
                                                    failures.append([index, "DQ-16", "duplicate company-year"])