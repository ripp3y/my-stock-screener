# --- 1. CONFIG & CACHING ---
st.set_page_config(page_title="Alpha Scout: Strategic Terminal", layout="wide")

# This "Cache" protects you from Rate Limits by saving data for 600 seconds (10 mins)
@st.cache_data(ttl=600)
def fetch_ticker_data(tickers):
    # Fetch 6 months of data in one bulk request
    return yf.download(tickers, period="6mo", group_by='ticker')

def get_technical_signals(data):
    # RSI & EMA Logic remains the same
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    ema_9 = data['Close'].ewm(span=9, adjust=False).mean()
    current_price = data['Close'].iloc[-1]
    current_ema = ema_9.iloc[-1]
    pct_dist = ((current_price - current_ema) / current_ema) * 100
    is_bottoming = (rsi.iloc[-1] > 30) and (rsi.iloc[-2] <= 30)
    return rsi, ema_9, pct_dist, is_bottoming

# --- 2. LIVE SCOUT ---
st.title("🚀 Alpha Scout: Strategic Command Center")
team_tickers = ["GEV", "BW", "PBR-A", "EQNR", "TPL", "SNDK", "MRNA"]

try:
    # Use the new cached function here
    data = fetch_ticker_data(team_tickers)
    
    # Rest of your metrics and chart code goes here...
