import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG & CACHING ---
st.set_page_config(page_title="Alpha Scout: Strategic Terminal", layout="wide")

# Static Analyst Targets for your Team
target_map = {
    "GEV": 863.61, "BW": 20.33, "PBR-A": 16.02, 
    "EQNR": 29.50, "TPL": 639.00, "SNDK": 95.00, 
    "MRNA": 115.00, "CIEN": 354.01, "TIGO": 73.20, "STX": 582.00
}

@st.cache_data(ttl=600) # Only talks to Yahoo every 10 mins to avoid blocks
def fetch_ticker_data(tickers):
    return yf.download(tickers, period="6mo", group_by='ticker')

def get_technical_signals(df):
    # RSI Momentum
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # 9-Day EMA (The "Boom Floor") and 50-Day EMA (Trend Health)
    ema_9 = df['Close'].ewm(span=9, adjust=False).mean()
    ema_50 = df['Close'].ewm(span=50, adjust=False).mean()
    
    current_price = df['Close'].iloc[-1]
    
    # Logic for Upward Channels & Dips
    is_upward
