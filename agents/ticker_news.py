# stock_multi_agent/agents/ticker_news.py

import requests
import os
from datetime import datetime, timedelta

def get_latest_news(ticker: str) -> list[str]:
    """
    Retrieves the latest news headlines related to a given stock ticker using NewsAPI.

    Args:
        ticker (str): The stock ticker symbol (e.g., "TSLA").

    Returns:
        list[str]: A list of news headlines.
                   Returns an empty list if no news is found or an error occurs.
    """
    if not ticker:
        print("Error: Ticker symbol is empty for news fetching.")
        return []

    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("NEWS_API_KEY not found in environment variables.")
        return []

    # Map tickers to company names for better search results with NewsAPI
    company_name_map = {
        "TSLA": "Tesla",
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corp.",
        "GOOGL": "Alphabet Inc.", # For Google/Alphabet
        "AMZN": "Amazon.com Inc.",
        "NVDA": "NVIDIA Corp.",
        "META": "Meta Platforms Inc."
    }
    # Use the mapped company name, or fall back to ticker if not found
    query_company = company_name_map.get(ticker.upper(), ticker)

    # Get news from the last 7 days to ensure recency
    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    # NewsAPI endpoint for 'everything'
    # 'qInTitle' helps focus on articles where the company is a main subject.
    # 'sortBy=relevancy' orders by relevance, 'pageSize=5' limits to top 5.
    url = (f"https://newsapi.org/v2/everything?"
           f"qInTitle=\"{query_company}\"&" # Quote query_company for exact phrase search
           f"from={from_date}&"
           f"language=en&"
           f"sortBy=relevancy&"
           f"pageSize=5&" # Limit to top 5 headlines
           f"apiKey={api_key}")

    news_headlines = []
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data.get("status") == "error":
            print(f"NewsAPI error for {ticker}: {data.get('message', 'Unknown error')}")
            return []
        if not data.get("articles"):
            print(f"No articles found for '{query_company}' from NewsAPI.")
            return []

        # Extract headlines (titles) from the articles
        for article in data["articles"]:
            if article.get("title") and article["title"] != "[Removed]": # Filter out removed articles
                news_headlines.append(article["title"])

        print(f"Successfully fetched {len(news_headlines)} news headlines for {ticker}.")
        # print(f"News for {ticker}: {news_headlines}") # Uncomment for debugging
        return news_headlines

    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error fetching news for {ticker}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while fetching news for {ticker}: {e}")
        return []