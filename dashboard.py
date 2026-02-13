import streamlit as st,json,time

st.set_page_config(layout="wide")
st.title("Trading Dashboard")

placeholder=st.empty()

while True:

    try:
        with open("data.json") as f:
            d=json.load(f)
    except:
        st.warning("Waiting for data...")
        time.sleep(2)
        continue

    with placeholder.container():

        c1,c2,c3=st.columns(3)
        c1.metric("Balance",d["balance"])
        c2.metric("PnL",d["pnl"])
        c3.metric("Drawdown",d["drawdown"])

        st.divider()

        c4,c5,c6=st.columns(3)
        c4.metric("Spread",d["spread"])
        c5.metric("Volatility",d["volatility"])
        c6.metric("Regime",d["regime"])

        st.success("Status: "+d["status"])

    time.sleep(2)