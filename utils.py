import time,json,hmac,hashlib,requests
from config import *

BASE="https://api.coindcx.com"

# SIGN REQUEST
def sign_payload(secret, body):
    body["timestamp"]=int(time.time()*1000)
    payload=json.dumps(body,separators=(',',':'))
    sig=hmac.new(secret.encode(),payload.encode(),hashlib.sha256).hexdigest()
    return payload,sig


# TELEGRAM
def send_alert(msg):
    if TELEGRAM_TOKEN=="":
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id":CHAT_ID,"text":msg},
            timeout=5
        )
    except:
        pass


# CANDLES
def get_candles():
    try:
        url=f"https://public.coindcx.com/market_data/candles?pair={PAIR_CANDLE}&interval=1m"
        data=requests.get(url,timeout=10).json()

        if not isinstance(data,list) or len(data)<20:
            return None

        import pandas as pd
        df=pd.DataFrame(data)
        df.columns=["open","high","low","volume","close","time"]
        df=df.astype(float)
        return df

    except Exception as e:
        print("Candles error:",e)
        return None


# SPREAD FROM TICKER
def spread():
    try:
        data=requests.get("https://api.coindcx.com/exchange/ticker",timeout=5).json()

        for coin in data:
            if coin["market"]==PAIR_TICKER:
                bid=float(coin["bid"])
                ask=float(coin["ask"])
                return ((ask-bid)/bid)*100,bid,ask

        return None,None,None

    except Exception as e:
        print("Spread error:",e)
        return None,None,None


# PLACE ORDER
def place_order(side,price,qty):

    if PAPER:
        print("PAPER",side,price)
        return

    body={
        "pair":PAIR_ORDER,
        "side":side,
        "order_type":"limit_order",
        "price_per_unit":price,
        "total_quantity":qty
    }

    payload,sig=sign_payload(API_SECRET,body)

    headers={
        "X-AUTH-APIKEY":API_KEY,
        "X-AUTH-SIGNATURE":sig,
        "Content-Type":"application/json"
    }

    r=requests.post(BASE+"/exchange/v1/orders/create",
                    data=payload,
                    headers=headers,
                    timeout=10)

    print("Order:",r.json())