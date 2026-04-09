import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

# --- 1. CONFIG & PRO STYLING ---
st.set_page_config(page_title="Alpha Scout Pro", layout="wide")

st.markdown("""
    <style>
    /* Metric Card Styling */
    div[data-testid="column"] { 
        padding: 15px; 
        border-radius: 10px;
        background: #1e1e1e;
        border-bottom: 2px solid #4CAF50;
    }
    /* Risk Footer Styling */
    .risk-footer {
        padding: 20px;
        background-color: #262626;
        border-radius: 10px;
        border: 1px solid #444;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

FINNHUB_KEY = "d7c0uh1r01quh9fc4hegd7c0uh1r01quh9fc4hf0"

team_intel = {
    "FIX": 1800.0, "ATRO": 95.0, "CENX": 86.0, "GEV": 1050.0,
    "TPL": 639.0, "CIEN": 430.0, "STX": 620.0
}

@st.cache_data(ttl=600)
def fetch_scout_data(tickers):
    syms = tickers + ["SPY", "^VIX"]
    try:
        df = yf.download(syms, period="1y", group_by='ticker')
        return df.ffill()
    except: return None

def fetch_insiders(symbol):
    url = f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={symbol}&token={FINNHUB_KEY}"
    try:
        r = requests.get(url).json()
        return pd.DataFrame(r.get('data', []))
    except: return pd.DataFrame()

# --- 2. ENGINE ---
st.title("🚀 Alpha Scout: Strategic Commander")
tickers = list(team_intel.keys())
all_data = fetch_scout_data(tickers)

if all_data is not None:
    spy_df = all_data["SPY"]
    stats = []
    
    for t in tickers:
        try:
            df = all_data[t].dropna()
            if df.empty: continue
            price = df['Close'].iloc[-1]
            day_pct = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            stats.append({"ticker": t, "price": price, "rs": rs, "daily": day_pct})
        except: continue

    # LEADERBOARD
    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    cols = st.columns(len(sorted_stats))
    for i, s in enumerate(sorted_stats):
        with cols[i]:
            st.metric(label=s['ticker'], value=f"${s['price']:.2f}", delta=f"{s['daily']:+.2f}%")
            st.caption(f"RS Score: **{s['rs']*100:+.1f}%**")

    st.divider()

    # --- 3. TARGET DRILL-DOWN ---
    sel = st.selectbox("Select Target for Analysis", [x['ticker'] for x in sorted_stats])
    tab1, tab2, tab3 = st.tabs(["📊 Technicals", "🕵️ Insider Intelligence", "🛡️ Risk Management"])

    with tab1:
        df_sel = all_data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], 
                        high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader(f"Owner Trading Activity: {sel}")
        insider_df = fetch_insiders(sel)
        if not insider_df.empty:
            # Color coding the Buy/Sell for clarity
            insider_df['Action'] = insider_df['change'].apply(lambda x: "🟢 BUY" if x > 0 else "🔴 SELL")
            display_df = insider_df[['transactionDate', 'name', 'Action', 'share', 'change', 'transactionPrice']].copy()
            st.dataframe(display_df.style.applymap(
                lambda x: 'color: #00ff00' if x == "🟢 BUY" else 'color: #ff4b4b' if x == "🔴 SELL" else '',
                subset=['Action']
            ), use_container_width=True)
        else:
            st.info("No recent Form 4 filings detected.")

    with tab3:
        df_r = all_data[sel].dropna()
        atr = (df_r['High'] - df_r['Low']).rolling(14).mean().iloc[-1]
        t_stop = df_r['Close'].iloc[-1] - (atr * 2.5)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("RS Score", f"{sorted_stats[0]['rs']*100:+.1f}%", 
                  help="Relative Strength: Measures if the stock is beating the S&P 500. Above 0% means it's an Alpha leader.")
        c2.metric("ATR (14d)", f"${atr:.2f}", 
                  help="Average True Range: The 'heartbeat' of the stock. High ATR means wide daily swings.")
        c3.metric("Trailing Stop", f"${t_stop:.2f}", delta=f"${df_r['Close'].iloc[-1]-t_stop:.2f} Buffer",
                  help="The 'Exit Floor'. Calculated by taking the current price and subtracting 2.5x the daily volatility (ATR).")

    # --- 4. THE PROFESSIONAL RISK FOOTER ---
    st.markdown('<div class="risk-footer">', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    
    with f1:
        st.markdown("**Core Strategy**")
        st.write("6-Month Growth / US Equities")
        st.caption("Focusing on high EPS and Alpha momentum.")
        
    with f2:
        st.markdown("**Risk Protocol**")
        if df_r['Close'].iloc[-1] < t_stop:
            st.error("⚠️ ALERT: PRICE BELOW STOP")
        else:
            st.success("🛡️ STATUS: TREND STABLE")
        st.caption("Manual exit triggered if price closes below Trailing Stop.")

    with f3:
        st.markdown("**Market Status**")
        vix = all_data["^VIX"]['Close'].iloc[-1]
        st.info(f"VIX: {vix:.2f}")
        st.caption("Volatility Index: Below 20 is favorable for growth.")
        
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("📡 Sync Issue: Verify API connection and Ticker list.")
