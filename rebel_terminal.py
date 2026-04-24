# MOCK LOGIC FOR YOUR TERMINAL: THE SOVEREIGNTY FILTER
def narrative_check(news_input):
    keywords_of_control = ["Consensus", "Safety", "Equity", "Standard of Care", "Regulated"]
    keywords_of_sovereignty = ["Independent", "Raw Data", "Natural", "Sovereign", "Decentralized"]
    
    control_score = sum(1 for word in keywords_of_control if word in news_input)
    sovereign_score = sum(1 for word in keywords_of_sovereignty if word in news_input)
    
    if control_score > sovereign_score:
        return "⚠️ WARNING: Institutional Narrative Detected (Potential Loop-Marketing)"
    return "✅ SIGNAL: Independent/Raw Data detected."
