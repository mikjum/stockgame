import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Osakekurssin seuranta")

# Käyttäjän syöte
ticker_symbol = st.text_input("Syötä yhtiön ticker (esim. AAPL, MSFT, NOKIA):", "AAPL")

# Lataa data
if ticker_symbol:
    ticker_data = yf.Ticker(ticker_symbol)
    hist = ticker_data.history(period="1y")

    st.subheader(f"{ticker_symbol} - Kurssikehitys 1 vuoden ajalta")
    st.line_chart(hist['Close'])

    st.subheader("Perustiedot")
    st.write(ticker_data.info)
