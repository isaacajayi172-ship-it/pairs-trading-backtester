import sqlite3
import pandas as pd

data = pd.read_csv("clean_prices.csv")

conn = sqlite3.connect("prices.db")

data.to_sql("prices", conn, if_exists = "replace", index = False)

cursor = conn.cursor()
cursor.execute("Select Date, MA FROM prices ORDER BY MA DESC LIMIT 5")
results = cursor.fetchall()

for row in results:
    print(row)

conn.close()

print(data.columns)