import pandas as pd

data = pd.read_csv("clean_prices.csv")

# Tests whether MA and V move together based on hsitorical 2025 data
# This will help justify building any strategy on top of it

correlation = data["MA"].corr(data["V"])

# if/else loop here to evaluate how strong the correlation is and whether it is negative or not

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

position = None      # are we currently in a trade?
trades = []             # will collect one record per completed trade
capital_gained_per_trade = 10000 # pretending to add 10,000 dollars every time we invest


# for loop to dictate what the action should be depending on the differing ratio between both MA and V each day

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

# calculating the profit in dollars 

total_profit = sum(t["profit_in_dollars"] for t in trades)
print("Total profit:", total_profit)

winning_trades = [t for t in trades if t["profit_in_dollars"] > 0]
win_rate = len(winning_trades) / len(trades)
print("Win rate:", win_rate)


print(sum(t["profit_in_dollars"] for t in trades))


# test to see if buy and holding strategy could out perform pairs strategy
# testing for well known limitation in pairs trading

first_MA = data["MA"].iloc[0]
last_MA = data["MA"].iloc[-1] # counting backwards
first_V = data["V"].iloc[0]
last_V = data["V"].iloc[-1]

MA_return = (last_MA - first_MA) / first_MA
V_return = (last_V - first_V) / first_V

buy_hold_profit = (MA_return * 10000) + (V_return * 10000)
print("Buy and hold profit:", buy_hold_profit)

data["cumulative_profit"] = 0.0
running_total = 0
for t in trades:
    running_total += t["profit_in_dollars"]
    data.loc[data["Date"] == t["exit_date"], "cumulative_profit"] = running_total


data["cumulative_profit"] = data["cumulative_profit"].replace(0, pd.NA).ffill().fillna(0)

print(data[data["cumulative_profit"] != 0])

running_max = data["cumulative_profit"].cummax()
drawdown = data["cumulative_profit"] - running_max
max_drawdown = drawdown.min()
print("Max drawdown:", max_drawdown)