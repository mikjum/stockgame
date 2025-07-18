import json
import os

DATA_FILE = "user_data.json"

# ✅ Lataa tallennetut tiedot
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"cash": 10000, "portfolio": {}}

# ✅ Tallenna tiedot
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ✅ Streamlit app
import streamlit as st
import yfinance as yf

st.title("Osakesimulaattori (Tallennuksella)")

data = load_data()

st.subheader(f"Käyttöraha: {data['cash']:.2f} USD")

ticker = st.text_input("Syötä yhtiön ticker:", "AAPL")
ticker_data = yf.Ticker(ticker)
price = ticker_data.history(period="1d")['Close'].iloc[-1]

st.write(f"Kurssi {ticker}: {price:.2f} USD")

buy_amount = st.number_input("Ostettavien osakkeiden määrä:", min_value=1, value=1)

if st.button("Osta"):
    total_cost = buy_amount * price
    if total_cost > data["cash"]:
        st.error("Ei tarpeeksi rahaa!")
    else:
        data["cash"] -= total_cost
        data["portfolio"][ticker] = data["portfolio"].get(ticker, 0) + buy_amount
        save_data(data)
        st.success(f"Ostit {buy_amount} kpl {ticker}-osakkeita hintaan {total_cost:.2f} USD")

# Näytä omistukset
st.subheader("Portfoliosi:")
for stock, qty in data["portfolio"].items():
    st.write(f"{stock}: {qty} kpl")
