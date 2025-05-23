

def get_ticker_from_query(query: str) -> str:

    query_lower = query.lower()

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
  
    words = query_lower.split()
    for word in words:
        if 2 <= len(word) <= 5 and word.isupper() and word.isalpha(): # All uppercase letters
            print(f"Attempting to use '{word.upper()}' as ticker from query.")
            return word.upper()

    print(f"Could not identify a clear ticker from query: '{query}'")
    return ""
