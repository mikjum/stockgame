import streamlit as st
import yfinance as yf
import json
from pathlib import Path
import pandas as pd
import subprocess
import os

# Tiedostopolku (samassa hakemistossa kuin app)
DATA_FILE = Path("user_data.json")

comission = 0.02

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"cash": 10000, "portfolio": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def git_commit_and_push(commit_message="Päivitetty käyttäjätieto"):
    subprocess.run(["git", "config", "--global", "user.email", "sinun@email.com"])
    subprocess.run(["git", "config", "--global", "user.name", "SinunGitHubNimi"])
    subprocess.run(["git", "add", str(DATA_FILE)])
    subprocess.run(["git", "commit", "-m", commit_message])
    
    github_token = os.getenv("GITHUB_TOKEN")
    repo_url = os.getenv("GITHUB_REPO_URL")
    if github_token and repo_url:
        push_url = repo_url.replace("https://", f"https://{github_token}@")
        subprocess.run(["git", "push", push_url])
    else:
        st.warning("GITHUB_TOKEN tai GITHUB_REPO_URL puuttuu!")

# Aloitus
st.title("Osakesalkun hallinta (Git-push)")

data = load_data()

TICKERS = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "META", "NVDA", "KO", "MCD", "NFLX"]
selected_ticker = st.selectbox("Valitse osake", TICKERS)

ticker_data = yf.Ticker(selected_ticker)
hist = ticker_data.history(period="3mo")

st.line_chart(hist["Close"])
st.write(f"Viimeisin kurssi: {hist['Close'].iloc[-1]:.2f} USD")
st.write(f"Käteinen: {data['cash']} USD")

# Osto
buy_amount = st.number_input("Ostosumma (USD)", min_value=0, step=100)
if st.button("Osta"):
    if buy_amount > data["cash"]:
        st.error("Ei tarpeeksi rahaa!")
    else:
        price = hist["Close"].iloc[-1]
        comission_to_pay = buy_amount * comission
        shares = buy_amount / price
        data["cash"] -= buy_amount
        data["cash"] -= comission_to_pay

        # Jos osaketta ei vielä portfoliosta löydy, alustetaan
        if selected_ticker not in data["portfolio"]:
            data["portfolio"][selected_ticker] = {"shares": 0, "value": 0}

        # Päivitetään osakkeiden määrä ja sijoitettu arvo
        data["portfolio"][selected_ticker]["shares"] += shares
        data["portfolio"][selected_ticker]["value"] += buy_amount
        data["portfolio"][selected_ticker]["value"] += comission_to_pay

        save_data(data)
        git_commit_and_push(f"Ostettiin {shares:.4f} kpl {selected_ticker}")
        st.success(f"Ostit {shares:.4f} kpl {selected_ticker} hintaan {price:.2f} USD sisältäen komission")
        

# Näytä salkku
st.subheader("Salkkusi")
if data["portfolio"]:
    for ticker, info in data["portfolio"].items():
        ticker_price = yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]
        shares = info["shares"]
        invested_value = info.get("value", 0)
        current_value = shares * ticker_price
        net_sell = current_value - current_value * comission
        st.write(f"{ticker}: {shares:.4f} kpl — Nykyarvo: {current_value:.2f} USD (Sijoitettu komissioineen: {invested_value:.2f} USD) Myynistä saatavissa oleva arvo: {net_sell:2f} USD")
else:
    st.write("Salkkusi on tyhjä.")
