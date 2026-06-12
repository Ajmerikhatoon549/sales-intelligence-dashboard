import pandas as pd
import sqlite3

# Extract
df = pd.read_csv("data/sales.csv")

# Transform
df["Revenue"] = df["Quantity"] * df["Price"]

# Load
conn = sqlite3.connect("sales.db")

df.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("ETL Pipeline Completed Successfully")