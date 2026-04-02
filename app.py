# --- STEP 5: SECTOR LEADERBOARD (FUTURE-PROOF VERSION) ---
st.subheader("🏆 Sector Alpha Leaderboard")
titans = ["XOM", "CVX", "GEV"]
combined = portfolio + titans
lb_data = []

for t in combined:
    d = yf.download(t, period="1mo")
    if not d.empty:
        p = d['Close'].values.flatten()
        lb_data.append({"Ticker": t, "1mo Return": round(((p[-1] - p[0]) / p[0]) * 100, 2)})

df = pd.DataFrame(lb_data).sort_values(by="1mo Return", ascending=False)

# FIX: Using width='stretch' to clear the deprecation warning
st.dataframe(df, width="stretch")
