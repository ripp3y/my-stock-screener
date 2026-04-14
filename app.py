import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. THE BRAIN (Neural Link) ---
# Update this section after our chats to sync the app's logic
STRATEGY_LOG = {
    "AUGO": "Rebalance window (Fri/Mon). Era Dorada approved ($382M). Watch $105 floor.",
    "MRVL": "2nm AI Breakout. Record $8.2B revenue. Strong Institutional buy signal.",
    "FIX": "Strong backlog. Neutral trend. Watching for next breakout trigger."
}

WATCHLIST = ["FIX", "ATRO", "GEV", "TPL", "STX", "MRVL", "SNDK", "AUGO"]

# --- 2. CONFIGURATION ---
st.set_page_config(
    page_title="Strategic US Terminal", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Better for mobile viewing
)

# Custom CSS for Mobile Styling
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="metric-container"] {
        background-color: #1E293B;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE FUNCTIONS ---
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

@st.cache_data(ttl=600)
def fetch_prices(ticker_list):
    try:
        # download as list to prevent UnhashableParamError
        return yf.download(list(ticker_list), period="2y", group_by='ticker').ffill()
    except Exception:
        return None

# --- 4. SIDEBAR COMMAND CENTER ---
with st.sidebar:
    st.title("🎚️ Neural Link")
    st.info("Direct sync with active chat strategy.")
    st.subheader("Tactical Memos")
    for ticker, note in STRATEGY_LOG.items():
        with st.expander(f"Order: {ticker}"):
            st.write(note)
    st.divider()
    st.caption("v2.0 Build | Powered by Gemini")

# --- 5. MAIN DISPLAY ---
all_data = fetch_prices(WATCHLIST)

if all_data is not None:
    # Header Selection
    sel = st.selectbox("Select Target", WATCHLIST)
    df_sel = all_data[sel].dropna()
    ticker_obj = yf.Ticker(sel)
    
    # RSI & Status Calculation
    df_sel['RSI'] = calculate_rsi(df_sel['Close'])
    current_rsi = df_sel['RSI'].iloc[-1]
    
    if current_rsi > 70: status, s_color = "OVERBOUGHT (CAUTION)", "#F87171"
    elif current_rsi < 30: status, s_color = "OVERSOLD (OPPORTUNITY)", "#4ADE80"
    else: status, s_color = "NEUTRAL (TRENDING)", "#93C5FD"

    st.markdown(f"### {sel} Status: <span style='color:{s_color}'>{status}</span>", unsafe_allow_html=True)
    
    # Display Neural Link Memo if available
    if sel in STRATEGY_LOG:
        st.info(f"**Chat Memo:** {STRATEGY_LOG[sel]}")

    # Mobile-Friendly Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Charts", "🛡️ Risk", "🕵️ Intel"])

    with tab1:
        fig = go.Figure(data=[go.Candlestick(
            x=df_sel.index, open=df_sel['Open'], high=df_sel['High'],
            low=df_sel['Low'], close=df_sel['Close'], name=sel
        )])
        fig.update_layout(
            template="plotly_dark", 
            xaxis_rangeslider_visible=False, 
            height=350, 
            margin=dict(l=0,r=0,t=0,b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.metric("RSI (14-Day)", f"{current_rsi:.2f}")

    with tab2:
        # RISK SCOUT BOX
        cp = df_sel['Close'].iloc[-1]
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        t_stop = cp - (atr * 2.5)
        stop_gap = cp - t_stop
        
        c1, c2 = st.columns(2)
        acc = c1.number_input("Account ($)", value=10000)
        risk_pct = c2.slider("Risk %", 0.5, 15.0, 3.0)
        
        shares = int((acc * (risk_pct / 100)) / stop_gap) if stop_gap > 0 else 0
        risk_f = (atr / cp) * 100
        
        box_color = "#4ADE80" if risk_f < 2.0 else "#FBBF24" if risk_f < 4.5 else "#F87171"
        
        st.markdown(f"""
            <div style="background-color: #1E3A8A; padding: 20px; border-radius: 12px; border-left: 10px solid {box_color};">
                <p style="color: #DBEAFE; font-size: 26px; margin: 0;"><b>Buy {shares} Shares</b></p>
                <p style="color: #93C5FD; font-size: 18px; margin: 5px 0;">Stop Loss: <b>${t_stop:.2f}</b></p>
                <hr style="border: 0.5px solid #3B82F6; margin: 15px 0;">
                <p style="color: #BFDBFE; font-size: 14px; margin: 0;">Risk Factor: <b>{risk_f:.2f}%</b></p>
            </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.subheader("Ownership Profile")
        try:
            holders = ticker_obj.major_holders
            if not holders.empty:
                st.write(holders)
        except: st.info("Ownership data currently restricted.")
        
        st.divider()
        st.subheader("Insider Moves")
        try:
            trades = ticker_obj.insider_transactions
            if not trades.empty:
                st.dataframe(trades[['Start Date', 'Insider', 'Transaction', 'Shares']].head(5), hide_index=True)
        except: st.warning("SEC Database Offline")

else:
    st.error("📡 Sync Issue: Connection lost.")
