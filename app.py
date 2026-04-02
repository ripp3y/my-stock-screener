# --- STEP 4: SECTOR LEADERBOARD ---
st.subheader("🏆 Sector Alpha Leaderboard")
titans = ["XOM", "CVX", "GEV"]
combined_list = portfolio + titans # portfolio = [PBR, CENX, EQNR, CNQ, CF]

leaderboard = []
for ticker in combined_list:
    data = yf.download(ticker, period="1mo")
    if not data.empty:
        prices = data['Close'].values.flatten()
        perf = ((prices[-1] - prices[0]) / prices[0]) * 100
        leaderboard.append({"Ticker": ticker, "Return": perf})

# Sort by performance
df_leader = pd.DataFrame(leaderboard).sort_values(by="Return", ascending=False)

# Highlight your actual holdings
def highlight_holdings(row):
    return ['background-color: #1e3a8a' if row.Ticker in portfolio else '' for _ in row]

st.table(df_leader.style.apply(highlight_holdings, axis=1))
