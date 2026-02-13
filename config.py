# ==========================================================
# A.P. ENTERPRISES - PROFIT OPTIMIZED CONFIGURATION
# ==========================================================

# ਤੁਹਾਡੀ API Keys (ਸੁਰੱਖਿਅਤ ਰੱਖੋ)
API_KEY = "d37616ccd1f29c02a48d0f1706800defdefde6865efd8dfe"
API_SECRET = "4fd1697fbff6a40b8694b8c8c7af87340431d7ffccb748cdcc41e9588b626893"

# ਟੈਸਟਿੰਗ ਮੋਡ
PAPER = True  

# ਸ਼ੁਰੂਆਤੀ ਬੈਲੇਂਸ (USDT ਵਿੱਚ)
INITIAL_BALANCE = 10000

# ================= STRATEGY SETTINGS (IMPORTANT) =================
# Grid Gap ਨੂੰ 0.4 ਤੋਂ ਵਧਾ ਕੇ 1.5 ਕੀਤਾ ਗਿਆ ਹੈ। 
# ਇਹ 1.2% (Tax + Fees) ਦੇ ਖਰਚੇ ਨੂੰ ਕੱਟ ਕੇ ਤੁਹਾਨੂੰ ਸ਼ੁੱਧ ਮੁਨਾਫ਼ਾ ਦੇਵੇਗਾ।
GRID_GAP = 1.5  

# Grid Levels ਘਟਾ ਕੇ 2 ਕੀਤੇ ਗਏ ਹਨ ਤਾਂ ਜੋ ਟੈਕਸ ਦਾ ਬੋਝ ਬਹੁਤ ਜ਼ਿਆਦਾ ਨਾ ਵਧੇ।
GRID_LEVELS = 2 

# ================= RISK FILTERS =================
# ਸਿਰਫ਼ ਉਦੋਂ ਟ੍ਰੇਡ ਕਰੋ ਜਦੋਂ ਮਾਰਕੀਟ ਵਿੱਚ ਕੀਮਤ ਦਾ ਫਰਕ (Spread) ਘੱਟ ਹੋਵੇ।
SPREAD_LIMIT = 0.20 

# ਜੇਕਰ ਨੁਕਸਾਨ 10% ਤੋਂ ਵਧੇਗਾ ਤਾਂ ਬੋਟ ਰੁਕ ਜਾਵੇਗਾ।
MAX_DRAWDOWN = 10 

# ਬਹੁਤ ਜ਼ਿਆਦਾ ਖ਼ਤਰਨਾਕ (Volatile) ਮਾਰਕੀਟ ਵਿੱਚ ਟ੍ਰੇਡਿੰਗ ਰੋਕੋ।
VOL_LIMIT = 1.5

# ================= SYMBOL SETTINGS =================
# CoinDCX ਦੇ ਸਹੀ ਪੇਅਰ (Pair) ਮੈਪਿੰਗ
PAIR_CANDLE = "B-BTC_USDT"
PAIR_TICKER = "BTCUSDT"
PAIR_ORDER = "BTCUSDT"

# ================= NOTIFICATIONS =================
TELEGRAM_TOKEN = ""
CHAT_ID = ""