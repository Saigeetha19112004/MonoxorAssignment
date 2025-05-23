# stock_multi_agent/agents/identify_ticker.py

def get_ticker_from_query(query: str) -> str:
    """
    Extracts the stock ticker symbol from a given query.
    This is a rule-based placeholder; a real system might use an LLM for robustness.

    Args:
        query (str): The user's query about a stock.

    Returns:
        str: The extracted stock ticker symbol (e.g., "TSLA" for Tesla).
             Returns an empty string if no ticker is found.
    """
    query_lower = query.lower()

    # Simple keyword mapping for common stocks
    if "tesla" in query_lower:
        return "TSLA"
    elif "apple" in query_lower:
        return "AAPL"
    elif "microsoft" in query_lower:
        return "MSFT"
    elif "google" in query_lower or "alphabet" in query_lower:
        return "GOOGL"
    elif "amazon" in query_lower:
        return "AMZN"
    elif "nvidia" in query_lower:
        return "NVDA"
    elif "meta" in query_lower or "facebook" in query_lower:
        return "META"
    # Add more mappings as needed

    # Very basic attempt to find a potential ticker-like string
    words = query_lower.split()
    for word in words:
        if 2 <= len(word) <= 5 and word.isupper() and word.isalpha(): # All uppercase letters
            print(f"Attempting to use '{word.upper()}' as ticker from query.")
            return word.upper()

    print(f"Could not identify a clear ticker from query: '{query}'")
    return ""