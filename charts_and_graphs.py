import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

data = pd.read_csv("results.csv")


data["ratio"] = data["MA"] / data["V"]
mean_ratio = data["ratio"].mean()
std_ratio = data["ratio"].std()
data["z_score"] = (data["ratio"] - mean_ratio) / std_ratio


# 1st chart to show z-zcore over time
plt.plot(data["Date"], data["z_score"])
plt.axhline(y = 2, color = "red", linestyle = "--")
plt.axhline(y = -2, color = "red", linestyle = "--")
plt.xlabel("Date")
plt.ylabel("z-score")
plt.title("MA/V price Ratio z-score over 2025")
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(10))
plt.xticks(rotation = 45)
plt.show()


# 2nd chart to compare both strategies
plt.plot(data["Date"], data["cumulative_profit"], label = "Pairs Strategy")
plt.plot(data["Date"], data["buyhold_total"], label = "Buy and Hold")
plt.xlabel("Date")
plt.ylabel("Profit gained in $")
plt.title("Pairs trading strategy vs Buy and Hold")
plt.legend()
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(10))
plt.xticks(rotation = 45)
plt.show()