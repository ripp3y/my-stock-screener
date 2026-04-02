import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px # New for the Heatmap

# --- STEP 1: DATA AGGREGATION ---
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF"]
titans = ["XOM", "CVX", "GEV"]
all_tickers = portfolio + titans

master_data = []
news_items = []

for t in all_tickers:
    tick = yf.Ticker(t)
    hist = tick.history(period="1mo")
    if not hist.empty:
        # Calculate Returns
        p = hist['Close'].values.flatten()
        abs_ret = round(((p[-1] - p[0]) / p[0]) * 100, 2)
        
        # Determine Sector for Heatmap
        sector = "Energy" if t in ["PBR", "EQNR", "CNQ", "XOM", "CVX"] else "Materials/Ind"
        
        master_data.append({
            "Ticker": t, 
            "Abs Return %": abs_ret, 
            "Sector": sector
        })
        
        # Collect News
        if len(news_items) < 5: # Limit to top 5 stories for speed
            stories = tick.news
            if stories:
                news_items.append({"ticker": t, "title": stories[0]['title'], "link": stories[0]['link']})

# --- STEP 2: DYNAMIC SECTOR HEATMAP ---
st.subheader("🔥 Sector Momentum Heatmap")
df = pd.DataFrame(master_data)

# Create a Treemap/Heatmap
fig = px.treemap(df, path=['Sector', 'Ticker'], values=[1]*len(df),
                 color='Abs Return %', 
                 color_continuous_scale='RdYlGn', # Red to Green
                 color_continuous_midpoint=0)
st.plotly_chart(fig, use_container_width=True)

# --- STEP 3: INTERACTIVE LEADERBOARD ---
st.subheader("🏆 Strategic Alpha Leaderboard")
st.dataframe(df.sort_values(by="Abs Return %", ascending=False), use_container_width=True, hide_index=True)

# --- STEP 4: LIVE NEWS FEED ---
st.sidebar.header("📰 Watchlist Intel")
for item in news_items:
    st.sidebar.markdown(f"**{item['ticker']}**: [{item['title']}]({item['link']})")
    st.sidebar.divider()

# --- STEP 5: RANKED FOOTER ---
ranked_footer = sorted(master_data, key=lambda x: x['Abs Return %'], reverse=True)
footer_str = " | ".join([f"{i['Ticker']}: {i['Abs Return %']}%" for i in ranked_footer])
st.caption(f"📅 **Last Month Performance (Ranked):** {footer_str}")
