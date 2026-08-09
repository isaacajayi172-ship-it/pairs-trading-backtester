import yfinance as yf

companies = ["MA", "V"]
data = yf.download(companies, start = "2025-01-01", end = "2025-12-31")
print(data)

closing_prices = data["Close"]
print(closing_prices)
closing_prices.to_csv("prices.csv")