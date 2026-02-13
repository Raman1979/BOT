import time, json, os, sys, subprocess, traceback, ta, threading
from config import *
from utils import *

# ================= AUTO GUI START =================
try:
    if not os.path.exists("kill.switch"):
        subprocess.Popen([sys.executable, "advanced_dashboard.py"])
except:
    pass

# ================= ACCOUNT & TAX SETTINGS =================
balance = INITIAL_BALANCE
peak = balance
inventory = 0  
last_buy_price = 0
FEE_RATE = 0.002  # 0.2% Exchange Fee
TDS_RATE = 0.01   # 1.0% TDS on Sell

# ================= REGIME FUNCTION (FIXED) =================
def regime(df):
    """ਮਾਰਕੀਟ ਦੇ ਟ੍ਰੈਂਡ ਨੂੰ ਪਛਾਣਨ ਲਈ"""
    try:
        df["adx"] = ta.trend.ADXIndicator(df.high, df.low, df.close).adx()
        df["atr"] = ta.volatility.AverageTrueRange(df.high, df.low, df.close).average_true_range()
        df["ema"] = df.close.ewm(span=50).mean()

        adx = df.adx.iloc[-1]
        atr = df.atr.iloc[-1]
        slope = df.ema.iloc[-1] - df.ema.iloc[-5]

        if adx > 25 and abs(slope) > df.close.iloc[-1]*0.001:
            return "TREND"
        if atr > df.atr.tail(50).mean()*1.5:
            return "VOLATILE"
        return "SIDEWAYS"
    except:
        return "SIDEWAYS"

# ================= DYNAMIC QTY CALCULATION =================
def get_dynamic_qty(current_price):
    try:
        if current_price <= 0: return 0.0001
        risk_amount = balance * 0.02 
        qty = risk_amount / current_price
        return round(qty, 6)
    except:
        return 0.0001

# ================= PRICE FEED =================
latest_price, latest_bid, latest_ask = 0, 0, 0
def price_feed():
    global latest_price, latest_bid, latest_ask
    while True:
        try:
            spr, bid, ask = spread()
            if bid and ask:
                latest_bid, latest_ask = bid, ask
                latest_price = (bid + ask) / 2
        except: pass
        time.sleep(1)

threading.Thread(target=price_feed, daemon=True).start()

# ================= LOG & CALCULATE TRADES =================
def log_trade(side, price, qty):
    global balance, inventory, last_buy_price
    
    raw_amt = price * qty
    trading_fee = raw_amt * FEE_RATE
    gross_p, net_p, taxes = 0, 0, 0
    
    if side == "BUY":
        total_impact = raw_amt + trading_fee
        taxes = trading_fee
        balance -= total_impact
        inventory += qty
        last_buy_price = price
    
    elif side == "SELL":
        tds = raw_amt * TDS_RATE
        taxes = trading_fee + tds
        impact_value = raw_amt - taxes
        
        gross_p = (price - last_buy_price) * qty if last_buy_price > 0 else 0
        net_p = gross_p - taxes
        balance += impact_value
        inventory -= qty

    trade = {
        "time": time.strftime("%H:%M:%S"),
        "side": side.upper(),
        "price": round(price, 2),
        "qty": qty,
        "cost": round(raw_amt, 2),
        "taxes": round(taxes, 2),
        "gross_p": round(gross_p, 2),
        "net_p": round(net_p, 2),
        "balance": round(balance, 2)
    }

    try:
        trades = json.load(open("trades.json")) if os.path.exists("trades.json") else []
        trades.append(trade)
        with open("trades.json", "w") as f:
            json.dump(trades[-50:], f, indent=2)
    except: pass

# ================= UPDATE DASHBOARD FILE =================
def update_dashboard_file(data):
    try:
        with open("data.json", "w") as f:
            json.dump(data, f)
    except: pass

# ================= MAIN STRATEGY LOOP =================
print("A.P. ENTERPRISES BOT STARTED")
while True:
    try:
        if os.path.exists("kill.switch"): 
            print("Kill switch detected. Stopping...")
            break

        df = get_candles()
        if df is None:
            time.sleep(5)
            continue

        state = regime(df) # ਹੁਣ ਇਹ ਗਲਤੀ ਨਹੀਂ ਦੇਵੇਗਾ
        spr, bid, ask = spread()
        price = latest_price if latest_price else df.close.iloc[-1]
        vol = df.close.pct_change().std() * 100

        if balance > peak: peak = balance
        dd = (peak - balance) / peak * 100 if peak > 0 else 0

        # --- RISK FILTERS ---
        if spr > SPREAD_LIMIT or dd > MAX_DRAWDOWN or vol > VOL_LIMIT:
            time.sleep(10)
            continue

        qty = get_dynamic_qty(price)
        
        # --- STRATEGY EXECUTION ---
        if state == "TREND":
            log_trade("BUY", price, qty)
        elif state == "SIDEWAYS":
            grid_qty = qty / GRID_LEVELS
            buy_p = price * (1 - GRID_GAP/100)
            sell_p = price * (1 + GRID_GAP/100)
            log_trade("BUY", buy_p, grid_qty)
            log_trade("SELL", sell_p, grid_qty)

        # Update GUI Data
        curr_equity = balance + (inventory * price)
        update_dashboard_file({
            "price": round(price, 2),
            "balance": round(curr_equity, 2),
            "pnl": round(curr_equity - INITIAL_BALANCE, 2),
            "drawdown": round(dd, 2),
            "spread": round(spr, 3),
            "volatility": round(vol, 3),
            "regime": state,
            "status": "RUNNING"
        })
        time.sleep(10)

    except Exception as e:
        print(f"Error in loop: {e}")
        time.sleep(10)


print("BOT STOPPED")