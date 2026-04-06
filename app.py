import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="Strategic US Terminal", page_icon="🛡️", layout="wide")

# --- 2. THE PAGE FUNCTIONS ---

def home_page():
    st.title("🏠 Command Center")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("PBR.A Yield on Cost", "596.1%", delta="Anchor Safe")
    with col2: st.metric("Diversification", "68.9%", delta="Target: 70.3%")
    with col3: st.metric("Top Sector", "Energy (XLE)", delta="+32.9% YTD")
    
    st.divider()
    
    # SECTOR ROTATION MATRIX
    st.subheader("🔄 Sector Rotation Matrix")
    sectors = {"Energy": "XLE", "Industrials": "XLI", "Materials": "XLB", "Tech": "XLK"}
    try:
        comp_data = yf.download(list(sectors.values()) + ["SPY"], period="6mo", interval="1d")['Close']
        rs_df = pd.DataFrame({name: comp_data[t] / comp_data["SPY"] for name, t in sectors.items()})
        st.line_chart(rs_df, height=300)
    except: st.warning("Market sync pending...")

    st.divider()
    
    # MANUAL HARVEST LOGGER
    st.subheader("📝 Manual Harvest Logger")
    with st.expander("Log Wednesday Sell (EQNR)"):
        p, q = st.number_input("Price ($)", value=41.67), st.number_input("Shares", value=49.15)
        if st.button("Confirm Harvest"): st.success(f"Harvested ${p*q:,.2f} to Dry Powder.")

def alpha_guardian():
    st.title("🛡️ Alpha Guardian: Sector Rankings")
    
    # Use 'PBR-A' to bypass the delisted error in image_c4378f
    tickers = ["EQNR", "PBR-A", "CENX", "CF", "GEV"]
    
    # Ranking Logic
    st.subheader("🏆 Ranked: Active Strategy")
    with st.status("Fetching Live Performance...", expanded=False):
        data = yf.download(tickers, period="5d", interval="1h")['Close']
        # Calculate 5-day % change for ranking
        pct_change = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100).sort_values(ascending=False)

    for ticker, perf in pct_change.items():
        with st.expander(f"⭐ {ticker} | Current: ${data[ticker].iloc[-1]:.2f} | {perf:+.2f}%"):
            # Drill-down: Info, News, and Chart
            t_obj = yf.Ticker(ticker)
            c1, c2 = st.columns([2, 1])
            with c1:
                st.line_chart(data[ticker], height=200)
            with c2:
                st.write(f"**{ticker} Intel**")
                st.caption(f"Sector: {t_obj.info.get('sector', 'N/A')}")
                st.caption(f"Target: ${t_obj.info.get('targetMeanPrice', 'N/A')}")
            
            st.write("**Latest Headlines:**")
            for news in t_obj.news[:2]:
                st.markdown(f"- [{news['title']}]({news['link']})")

def research_hub():
    st.title("🔍 Deep Research Hub")
    ticker = st.text_input("Enter Ticker for 100% Club Benchmarking", value="KOS").upper()
    if ticker:
        t = yf.Ticker(ticker)
        st.line_chart(t.history(period="1y")['Close'])
        st.write(f"Analysis for {ticker} updated as of {datetime.now().strftime('%Y-%m-%d')}")

# --- 3. NAVIGATION ---
pg = st.navigation([
    st.Page(home_page, title="Home", icon="🏠"),
    st.Page(alpha_guardian, title="Guardian", icon="🛡️"),
    st.Page(research_hub, title="Research", icon="🔍")
])
pg.run()
