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

