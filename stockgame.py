import streamlit as st
import yfinance as yf
import json
from pathlib import Path
import pandas as pd

# Tiedostopolku (sama kuin repossa)
DATA_FILE = Path("user_data.json")

# Funktio datan lukemiseen
def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"cash": 10000, "portfolio": {}}

# Funktio datan tallentamiseen
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Streamlit-käyttöliittymä alkaa tästä
st.title("Osakesalkun hallinta")

# Alustetaan käyttäjätieto
data = load_data()

# Valmiit tickerit (voit lisätä tähän)
TICKERS = ["AAPL", "MSFT", "TSLA", "GOOGL"]

selected_ticker = st.selectbox("Valitse osake", TICKERS)

# Näytetään kurssikehitys (3 kk)
ticker_data = yf.Ticker(selected_ticker)
hist = ticker_data.history(period="3mo")

st.line_chart(hist["Close"])
st.write(f"Viimeisin kurssi: {hist['Close'].iloc[-1]:.2f} USD")

st.write(f"Käteinen tililläsi: {data['cash']} USD")

# Osto
buy_amount = st.number_input("Ostosumma (USD)", min_value=0, step=100)
if st.button("Osta"):
    if buy_amount > data["cash"]:
        st.error("Ei tarpeeksi rahaa!")
    else:
        price = hist["Close"].iloc[-1]
        shares = buy_amount / price
        data["cash"] -= buy_amount
        data["portfolio"][selected_ticker] = data["portfolio"].get(selected_ticker, 0) + shares
        save_data(data)
        st.success(f"Ostit {shares:.4f} kpl osakkeita {selected_ticker} hintaan {price:.2f} USD")
        st.experimental_rerun()

# Näytä salkku
st.subheader("Salkkusi")
if data["portfolio"]:
    for ticker, shares in data["portfolio"].items():
        ticker_price = yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]
        st.write(f"{ticker}: {shares:.4f} kpl — Arvo: {shares * ticker_price:.2f} USD")
else:
    st.write("Salkkusi on tyhjä.")


