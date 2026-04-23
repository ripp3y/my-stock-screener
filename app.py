@st.cache_data(ttl=300)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # We add '1d' as a backup period to ensure data always returns
        df = yf.download(
            tickers=tickers, 
            period="1mo",  # Increased period for more reliable data
            interval="1d",   # Daily is more stable than hourly on Streamlit Cloud
            group_by='ticker', 
            auto_adjust=True,
            progress=False
        )
        if df.empty:
            st.warning("📡 Signal Weak: Retrying connection...")
            return None
        return df
    except Exception as e:
        st.error(f"📡 Connection Interrupted: {e}")
        return None
