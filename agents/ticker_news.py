import requests
import os
from datetime import datetime, timedelta

def get_latest_news(ticker: str) -> list[str]:
   
    if not ticker:
        print("Error: Ticker symbol is empty for news fetching.")
        return []

    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("NEWS_API_KEY not found in environment variables.")
        return []

    company_name_map = {
        "TSLA": "Tesla",
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corp.",
        "GOOGL": "Alphabet Inc.", 
        "AMZN": "Amazon.com Inc.",
        "NVDA": "NVIDIA Corp.",
        "META": "Meta Platforms Inc."
    }
   
    query_company = company_name_map.get(ticker.upper(), ticker)

    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    url = (f"https://newsapi.org/v2/everything?"
           f"qInTitle=\"{query_company}\"&"
           f"from={from_date}&"
           f"language=en&"
           f"sortBy=relevancy&"
           f"pageSize=5&"
           f"apiKey={api_key}")

    news_headlines = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "error":
            print(f"NewsAPI error for {ticker}: {data.get('message', 'Unknown error')}")
            return []
        if not data.get("articles"):
            print(f"No articles found for '{query_company}' from NewsAPI.")
            return []

        for article in data["articles"]:
            if article.get("title") and article["title"] != "[Removed]":
                news_headlines.append(article["title"])

        print(f"Successfully fetched {len(news_headlines)} news headlines for {ticker}.")
        
        return news_headlines

    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error fetching news for {ticker}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while fetching news for {ticker}: {e}")
        return []
