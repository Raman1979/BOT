import json
import matplotlib.pyplot as plt

# ================= LOAD TRADES =================
with open("trades.json") as f:
    trades=json.load(f)

if len(trades)<2:
    print("Not enough trades")
    exit()

pairs=[]
equity=[0]
balance=0

# ================= PAIR TRADES =================
for i in range(1,len(trades)):

    a=trades[i-1]
    b=trades[i]

    if a["side"]=="BUY" and b["side"]=="SELL":

        profit=b["price"]-a["price"]
        balance+=profit

        pairs.append({
            "buy_time":a["time"],
            "buy_price":a["price"],
            "sell_time":b["time"],
            "sell_price":b["price"],
            "profit":profit
        })

        equity.append(balance)

# ================= STATS =================
profits=[p["profit"] for p in pairs]

wins=sum(1 for p in profits if p>0)
loss=sum(1 for p in profits if p<=0)

total=len(profits)
net=sum(profits)
avg=net/total if total else 0
winrate=wins/total*100 if total else 0


# ================= REPORT =================
print("\n========== TRADE TABLE ==========\n")

for t in pairs:
    print(
        t["buy_time"],
        "BUY",t["buy_price"],
        "→",
        t["sell_time"],
        "SELL",t["sell_price"],
        "| PnL:",round(t["profit"],2)
    )

print("\n========== SUMMARY ==========\n")

print("Total Trades:",total)
print("Wins:",wins)
print("Loss:",loss)
print("Winrate:",round(winrate,2),"%")

print("\nNet Profit:",round(net,2))
print("Average:",round(avg,2))
print("Best Trade:",max(profits))
print("Worst Trade:",min(profits))

# ================= DRAWDOWN =================
peak=0
dd=0

for x in equity:
    if x>peak:
        peak=x
    d=peak-x
    if d>dd:
        dd=d

print("Max Drawdown:",round(dd,2))

print("\n==============================\n")


# ================= EQUITY GRAPH =================
plt.plot(equity)
plt.title("Equity Curve")
plt.xlabel("Trades")
plt.ylabel("Profit")
plt.show()