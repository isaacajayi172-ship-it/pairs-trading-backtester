import pandas as pd

data = pd.read_csv("prices.csv", index_col = "Date")
print(data.isna().sum())
print(data.shape)


data = data.dropna()
print(data.shape)

data.to_csv("clean_prices.csv")