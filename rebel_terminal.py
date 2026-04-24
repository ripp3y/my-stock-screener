# SOVEREIGNTY TERMINAL V2.0 - UNBOUND LOGIC
def narrative_geiger(text_input):
    # The keywords of the "Standard of Care" and "Institutional Safety"
    architect_keywords = ["Mandate", "Standardized", "Digital ID", "Global Consensus", "Sustainability"]
    
    score = sum(1 for word in architect_keywords if word in text_input)
    
    if score > 2:
        return "⚠️ NARRATIVE DETECTED: Scripted Institutional Logic Found."
    return "✅ SIGNAL: Independent/Raw Data detected."
