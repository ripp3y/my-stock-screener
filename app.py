import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG & UPDATED TEAM ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

# Updated targets based on your latest portfolio additions and upgrades
target_map = {
    "FIX": 1800.00, "ATRO": 95.00, "CENX": 86.00, 
    "GEV": 863.61, "BW": 20.33, "TPL": 639.00, 
    "CIEN": 430.00, "STX": 620.00, "PBRA": 16.20,
    "SNDK": 95.00, "MRNA": 115.00, "TIGO": 73.20
}

@st.cache_data(ttl=600)
def fetch_ticker_data(tickers):
    data = yf.download(tickers, period="1y", group_by='ticker')
    infos = {t: yf.Ticker(t).info for t in tickers}
    return data, infos

def get_signals(df, target):
    price = df['Close'].iloc[-1]
    ema_9 = df['Close'].ewm(span=9, adjust=False).mean()
    ema_50 = df['Close'].ewm(span=50, adjust=False).mean()
    
    cushion = ((price - ema_9.iloc[-1]) / ema_9.iloc[-1]) * 100
    is_up = ema_50.iloc[-1] > ema_50.iloc[-5]
    is_dip = price < ema_9.iloc[-1] and price > ema_50.iloc[-1]
    
    # Risk Score: How far is price from analyst target?
    # Negative % means room to run. Positive % means overextended.
    risk_score = ((price - target) / target) * 100
    return cushion, is_up, is_dip, risk_score

# --- 2. DATA PROCESSING ---
st.title("🚀 Alpha Scout: Strategic Command")
team_tickers = list(target
