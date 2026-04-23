@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # Changed period to '2mo' (60 days) to give you the full trend.
        # Interval '1d' ensures the charts load instantly without buffering.
        df = yf.download(
            tickers=tickers, 
            period="2mo", 
            interval="1d", 
            group_by='ticker', 
            auto_adjust=True,
            progress=False
        )
        return df if not df.empty else None
    except Exception as e:
        return None

# --- [UI UPDATE FOR RECON TAB] ---
# In your Tab 1 code, update the 'move' calculation to reflect the new period
with tab_recon:
    # ... (existing portfolio code)
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                ticker_data = data[t]
                curr = ticker_data['Close'].iloc[-1]
                # Compare to 30 days ago (approx 20-22 trading days)
                start_price = ticker_data['Close'].iloc[0] 
                total_move = ((curr - start_price) / start_price) * 100
                
                recon_list.append({
                    "Ticker": t, 
                    "Price": f"${curr:.2f}", 
                    "Trend Move": f"{total_move:+.2f}%", # Now shows 60-day performance
                    "Mission Status": status_map.get(t, "🟢 Tracking")
                })
            except: continue
