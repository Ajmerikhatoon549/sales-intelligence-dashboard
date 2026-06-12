import pandas as pd
import random
from datetime import datetime, timedelta

regions = ["North", "South", "East", "West"]
products = ["Laptop", "Mobile", "Chair", "Table"]

data = []

for i in range(1, 1001):
    date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 365))

    product = random.choice(products)

    if product == "Laptop":
        price = 50000
    elif product == "Mobile":
        price = 20000
    elif product == "Chair":
        price = 3000
    else:
        price = 10000

    data.append([
        1000 + i,
        date.strftime("%Y-%m-%d"),
        random.choice(regions),
        product,
        random.randint(1, 10),
        price
    ])

df = pd.DataFrame(
    data,
    columns=["OrderID", "Date", "Region", "Product", "Quantity", "Price"]
)

df.to_csv("data/sales.csv", index=False)

print("1000 records generated")