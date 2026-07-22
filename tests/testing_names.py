import sqlite3
import pandas as pd

conn = sqlite3.connect("/Users/arunkumar/Desktop/N100_financial_intelligence/db/n100.db")

df = pd.read_sql("PRAGMA table_info(financial_ratios)", conn)

print(df["name"])

conn.close()