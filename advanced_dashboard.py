import tkinter as tk
import json, threading, time, os

root = tk.Tk()
root.title("A.P. ENTERPRISES - QUANT TERMINAL")
root.geometry("1000x850")
root.configure(bg="#0b0f14")

# ================= TOP HEADER =================
title = tk.Label(root, text="A.P. ENTERPRISES AI TRADING TERMINAL", 
               font=("Segoe UI", 20, "bold"), fg="#00eaff", bg="#0b0f14")
title.pack(pady=15)

# ================= LIVE METRICS CONTAINER =================
container = tk.Frame(root, bg="#0b0f14")
container.pack(fill="x", padx=20)

labels = {}
# ਉਹ ਸਾਰੇ ਫੀਲਡ ਜੋ ਅਸੀਂ ਲਾਈਵ ਦੇਖਣੇ ਹਨ
fields = [
    ("price", "Live Price (USDT)"),
    ("balance", "Current Equity"),
    ("pnl", "Total PnL"),
    ("drawdown", "Max Drawdown %"),
    ("spread", "Market Spread %"),
    ("volatility", "Volatility"),
    ("regime", "Market Regime"),
    ("status", "System Status")
]

# ਗਰਿੱਡ ਲੇਆਉਟ ਰਾਹੀਂ ਡੱਬੇ ਬਣਾਉਣਾ
for i, (key, label) in enumerate(fields):
    row = i // 4
    col = i % 4
    
    box = tk.Frame(container, bg="#111827", bd=1, relief="flat")
    box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    container.grid_columnconfigure(col, weight=1)

    tk.Label(box, text=label, fg="#9ca3af", bg="#111827", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(5, 0))
    
    val_label = tk.Label(box, text="---", fg="#22c55e", bg="#111827", font=("Segoe UI", 16, "bold"))
    val_label.pack(anchor="w", padx=10, pady=(0, 10))
    labels[key] = val_label

# ================= TRADE HISTORY TABLE =================
table_title = tk.Label(root, text="RECENT TRADE LOGS (INCL. TAX & NET PROFIT)", 
                     fg="white", bg="#0b0f14", font=("Segoe UI", 12, "bold"))
table_title.pack(pady=(20, 5))

# Listbox for trades
table = tk.Listbox(root, width=130, height=18, bg="#111827", fg="white", 
                 font=("Consolas", 10), bd=0, highlightthickness=0)
table.pack(padx=20, pady=10)

# ================= COLOR LOGIC =================
def get_color(key, value):
    try:
        val_float = float(value)
        if key in ["pnl", "net_p"]:
            return "#22c55e" if val_float >= 0 else "#ef4444"
        if key == "drawdown":
            return "#ef4444" if val_float > 5 else "#22c55e"
    except:
        pass
    if value == "TREND": return "#3b82f6"
    if value == "SIDEWAYS": return "#eab308"
    return "#22c55e"

# ================= UPDATE LOOP =================
def updater():
    while True:
        try:
            # 1. ਲਾਈਵ ਮੀਟਰਿਕਸ ਅਪਡੇਟ ਕਰੋ (data.json ਤੋਂ)
            if os.path.exists("data.json"):
                with open("data.json", "r") as f:
                    d = json.load(f)
                for k in labels:
                    if k in d:
                        val_text = str(d[k])
                        labels[k].config(text=val_text, fg=get_color(k, val_text))

            # 2. ਟ੍ਰੇਡ ਹਿਸਟਰੀ ਅਪਡੇਟ ਕਰੋ (trades.json ਤੋਂ)
            if os.path.exists("trades.json"):
                with open("trades.json", "r") as f:
                    trades = json.load(f)
                table.delete(0, tk.END)
                
                header = f"{'TIME':<10} | {'SIDE':<5} | {'PRICE':<12} | {'COST':<10} | {'TAX':<8} | {'NET PNL':<10}"
                table.insert(tk.END, header)
                table.insert(tk.END, "-"*120)
                
                for t in reversed(trades):
                    row = f"{t['time']:<10} | {t.get('side',''):<5} | {t.get('price',0):<12.2f} | {t.get('cost',0):<10.2f} | {t.get('taxes',0):<8.2f} | {t.get('net_p',0):<10.2f}"
                    table.insert(tk.END, row)
        except Exception as e:
            print(f"GUI Update Error: {e}")
        
        time.sleep(1) # ਹਰ 1 ਸਕਿੰਟ ਬਾਅਦ ਅਪਡੇਟ

# Thread ਚਲਾਓ
threading.Thread(target=updater, daemon=True).start()

# ================= STOP BUTTON =================
def stop_bot():
    open("kill.switch", "w").close()
    root.destroy()

stop_btn = tk.Button(root, text="STOP TRADING BOT", command=stop_bot, 
                   bg="#ef4444", fg="white", font=("Segoe UI", 12, "bold"), 
                   padx=30, pady=10, relief="flat")
stop_btn.pack(pady=20)

root.mainloop()