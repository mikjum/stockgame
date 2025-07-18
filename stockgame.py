import json
import os
import streamlit as st
import yfinance as yf

DATA_FILE = "user_data.json"
TICKERS = ["AAPL", "MSFT", "GOOG", "NVDA", "NOKIA", "TSLA"]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"cash": 10000, "portfolio": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

st.title("Osakesimulaattori (Historiallisella kurssikäyrällä)")

data = load_data()
st.subheader(f"Käyttöraha: {data['cash']:.2f} USD")

selected_ticker = st.selectbox("Valitse yhtiö:", TICKERS)

ticker_data = yf.Ticker(selected_ticker)

# ✅ Haetaan 3kk historian hintadata
hist = ticker_data.history(period="3mo")

# ✅ Nykyinen hinta
current_price = hist['Close'].iloc[-1]
st.write(f"Kurssi {selected_ticker} (nyt): {current_price:.2f} USD")

# ✅ Piirretään kurssikäyrä
st.line_chart(hist['Close'])

# ✅ Osto-osio
buy_amount = st.number_input("Ostettavien osakkeiden määrä:", min_value=1, value=1)

if st.button("Osta"):
    total_cost = buy_amount * current_price
    if total_cost > data["cash"]:
        st.error("Ei tarpeeksi rahaa!")
    else:
        data["cash"] -= total_cost
        data["portfolio"][selected_ticker] = data["portfolio"].get(selected_ticker, 0) + buy_amount
        save_data(data)
        st.success(f"Ostit {buy_amount} kpl {selected_ticker}-osakkeita hintaan {total_cost:.2f} USD")

# ✅ Näytä portfolio
st.subheader("Portfoliosi:")
for stock, qty in data["portfolio"].items():
    st.write(f"{stock}: {qty} kpl")
