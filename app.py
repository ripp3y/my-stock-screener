import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

# --- 1. SETTINGS & REFINED MOBILE CSS ---
st.set_page_config(page_title="Alpha Scout", layout="wide")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px !important; color: #ffffff; }
    div[data-testid="column"] { 
        padding: 15px; 
        border-radius: 10px;
        background: #1e1e1e;
        margin-bottom: 10px;
        border-left: 5px solid #4CAF50;
    }
    /* Institutional highlight box */
    .inst-box {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #4CAF50;
        text-align: center;
        margin-bottom: 20px;
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
    except:
        return None

def fetch_insider_data(symbol):
    url = f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={symbol}&token={FINNHUB_KEY}"
    try:
        r = requests.get(url).json()
        return pd.DataFrame(r.get('data', []))
    except:
        return pd.DataFrame()

# --- 2. ENGINE ---
st.title("🚀 Alpha Scout: Strategic Commander")
tickers = list(team_intel.keys())
all_data = fetch_scout_data(tickers)

if all_data is not None:
    stats = []
    spy_df = all_data["SPY"]
    
    for t in tickers:
        try:
            df = all_data[t].dropna()
            if df.empty: continue
            price = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2]
            day_pct = ((price - prev_close) / prev_close) * 100
            rs = (df['Close'].pct_change(20).iloc[-1]) - (spy_df['Close'].pct_change(20).iloc[-1])
            stats.append({"ticker": t, "price": price, "rs": rs, "daily": day_pct})
        except: continue

    sorted_stats = sorted(stats, key=lambda x: x['rs'], reverse=True)
    
    for s in sorted_stats:
        with st.container():
            c1, c2 = st.columns([2, 1])
            c1.metric(label=f"Ticker: {s['ticker']}", value=f"${s['price']:.2f}")
            c2.metric(label="Day %", value="", delta=f"{s['daily']:+.2f}%")
            st.caption(f"Relative Strength vs S&P: **{s['rs']*100:+.1f}%**")

    st.divider()

    # --- 3. TARGET FOCUS ---
    sel = st.selectbox("Select Target", [x['ticker'] for x in sorted_stats])
    t1, t2, t3 = st.tabs(["📊 Charts", "🛡️ Risk Scout", "🕵️ Insiders"])

    with t1:
        df_sel = all_data[sel].dropna()
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], 
                        high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        df_r = all_data[sel].dropna()
        atr = (df_r['High'] - df_r['Low']).rolling(14).mean().iloc[-1]
        current_price = df_r['Close'].iloc[-1]
        t_stop = current_price - (atr * 2.5)
        
        # Logic for Color-Coded Trailing Stop
        buffer = current_price - t_stop
        if buffer > (atr * 1.5):
            stop_color = "normal"  # Green
            stop_suffix = "↑ Strong Buffer"
        elif buffer > 0:
            stop_color = "off"     # Yellow/Gray
            stop_suffix = "- Tightening"
        else:
            stop_color = "inverse" # Red
            stop_suffix = "↓ BREACHED"

        st.metric("ATR Volatility", f"${atr:.2f}", 
                  help="Measures current daily 'noise'. Higher ATR means wider swings.")
        
        st.metric(
            label="Trailing Stop", 
            value=f"${t_stop:.2f}", 
            delta=f"${buffer:.2f} {stop_suffix}",
            delta_color=stop_color,
            help="Volatility-adjusted floor. Green indicates a healthy trend buffer. Red means the trend is likely broken."
        )

    with t3:
        # 1. Institutional Ownership Header
        try:
            ticker_info = yf.Ticker(sel).info
            inst_own = ticker_info.get('heldPercentInstitutions', 0) * 100
            st.markdown(f"""
                <div class="inst-box">
                    <h3 style='margin:0; color:#4CAF50;'>Institutional Ownership</h3>
                    <h1 style='margin:0;'>{inst_own:.1f}%</h1>
                    <p style='margin:0; color:#888;'>Percentage of shares held by major funds and banks</p>
                </div>
            """, unsafe_allow_html=True)
        except:
            st.info("Institutional data currently unavailable.")

        # 2. Insider Table
        st.subheader("Recent Insider Activity (Form 4)")
        insider_df = fetch_insider_data(sel)
        if not insider_df.empty:
            view_cols = [c for c in ['transactionDate', 'name', 'share', 'change'] if c in insider_df.columns]
            st.dataframe(insider_df[view_cols], use_container_width=True)
        else:
            st.info("No recent insider Form 4 filings found.")

else:
    st.error("📡 Connection lost. Check API connectivity.")
