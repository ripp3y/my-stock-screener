import streamlit as st
import pandas as pd
import requests
import io

# --- [1. CONFIG] ---
st.set_page_config(page_title="STEALTH STAND v11.10")

# --- [2. THE TUNED FUNCTION] ---
def get_data_stealth(ticker):
    try:
        # We use a different URL format that is often less guarded
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?interval=1d&events=history"
        
        # We upgraded the digital 'ID' to look like a standard Chrome browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            return df
        else:
            # This will tell us EXACTLY why it's failing (403, 404, etc.)
            st.error(f"Access Denied for {ticker}. Error Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Mechanical Failure: {e}")
        return None

# --- [3. INTERFACE] ---
st.title("📟 STEALTH STAND v11.10")
st.write("Engine is clear. Testing the fuel line (Yahoo Connection)...")

if st.button("RE-FIRE ENGINE"):
    with st.spinner("Injecting Stealth Headers..."):
        for symbol in ["NVTS", "BTC-USD"]:
            data = get_data_stealth(symbol)
            if data is not None:
                st.success(f"Connection Established: {symbol}")
                st.metric(f"{symbol} Price", f"${data['Close'].iloc[-1]:.2f}")
                st.line_chart(data['Close'].tail(20))
