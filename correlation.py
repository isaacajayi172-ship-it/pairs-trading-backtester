import pandas as pd

data = pd.read_csv("clean_prices.csv")

# Tests whether MA and V move together based on hsitorical 2025 data
# This will help justify building any strategy on top of it

correlation = data["MA"].corr(data["V"])

if correlation > 1:
    print(correlation, "Error, value should not be greater than 1!")
elif correlation > 0.7:
    print(correlation, "That is a very strong positive correlation!")
elif correlation > 0.5:
    print(correlation, "That is a moderately positive correlation!")
elif correlation > 0:
    print(correlation, "That is a weak positive correlation!")
elif correlation > -0.5:
    print(correlation, "That is a weak neagtive correlation!")
elif correlation > -0.7:
    print(correlation, "That is a moderately negative correlation!")
elif correlation > -1:
    print(correlation, "That is a strong positive correlation!")
elif correlation < -1:
    print(correlation, "Error, value should not be less than -1")

# calculationg ratio
data["ratio"] = data["MA"] / data["V"]

# ratio should roughly stay constant throughout
mean_ratio = data["ratio"].mean()
std_ratio = data["ratio"].std()

data["z_score"] = (data["ratio"] - mean_ratio) / std_ratio

def get_signal(z):
    if z > 2:
        return "Sell MA and Buy V"
    elif z < -2:
        return "Buy MA and Sell V"
    else:
        return "Hold"

signals = []
for z in data["z_score"]:
    signals.append(get_signal(z))
data["signal"] = signals

print(data["signal"].value_counts())

position = None      # comment: are we currently in a trade? None = no, otherwise store entry details
trades = []             # comment: will collect one record per completed trade
capital_gained_per_trade = 10000

for i in range(len(data)):
    z = data["z_score"].iloc[i]
    date = data["Date"].iloc[i]

    if position is None:
        if z > 2:
            position = {"entry_date": date, "entry_z": z, "entry_ratio": data["ratio"].iloc[i], "type": "SELL MA / BUY V"}
        elif z < -2:
            position = {"entry_date": date, "entry_z": z, "entry_ratio": data["ratio"].iloc[i], "type": "BUY MA / SELL V"}
    else:
        if abs(z) < 0.5:
            profit = abs(position["entry_z"]) - abs(z)

            exit_ratio = data["ratio"].iloc[i]
            pct_return = abs(position["entry_ratio"] - exit_ratio) / position["entry_ratio"]
            profit_in_dollars = pct_return * capital_gained_per_trade

            trades.append({
                "entry_date": position["entry_date"],
                "exit_date": date,
                "type": position["type"],
                "profit_in_dollars": profit_in_dollars
            })
            position = None

print(len(trades), "trades completed")
for t in trades:
    print(t)


total_profit = sum(t["profit_in_dollars"] for t in trades)
print("Total profit:", total_profit)

winning_trades = [t for t in trades if t["profit_in_dollars"] > 0]
win_rate = len(winning_trades) / len(trades)
print("Win rate:", win_rate)


print(sum(t["profit_in_dollars"] for t in trades))