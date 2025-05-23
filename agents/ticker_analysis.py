# stock_multi_agent/agents/ticker_analysis.py

# This agent synthesizes information from price data and news.
# It does NOT make direct external API calls for new data.
# It could be enhanced to use an LLM for more sophisticated sentiment analysis or summary generation.

def analyze_stock(ticker: str, current_price: float, price_change: float, news_headlines: list[str]) -> str:
    """
    Analyzes stock price and news to provide insights.

    Args:
        ticker (str): The stock ticker symbol.
        current_price (float): The current price of the stock.
        price_change (float): The percentage change in stock price.
        news_headlines (list[str]): A list of news headlines related to the stock.

    Returns:
        str: A summary analysis of the stock.
    """
    if not ticker:
        return "Cannot analyze stock without a ticker."

    analysis_parts = [f"Comprehensive Stock Analysis for {ticker}:"]

    # --- Price Analysis ---
    if price_change > 0.5: # Significant rise
        analysis_parts.append(f"The stock has seen a notable increase of {price_change:.2f}% today, currently trading at ${current_price:.2f}.")
    elif price_change < -0.5: # Significant fall
        analysis_parts.append(f"The stock has experienced a significant drop of {abs(price_change):.2f}% today, now at ${current_price:.2f}.")
    elif price_change != 0: # Minor fluctuation (between -0.5% and +0.5%, excluding 0)
        analysis_parts.append(f"The stock is showing a slight movement of {price_change:.2f}% today, with the current price at ${current_price:.2f}.")
    else: # Stable
        analysis_parts.append(f"The stock price for {ticker} is stable today, holding at ${current_price:.2f}.")

    # --- News Analysis (simple keyword-based sentiment) ---
    positive_keywords = ["gain", "rise", "grow", "expansion", "record", "strong", "beats", "innovat", "launch", "partnership", "success", "optimistic", "acquisition", "revenue", "profit"]
    negative_keywords = ["fall", "drop", "decline", "loss", "misses", "warns", "delay", "investigation", "scandal", "lawsuit", "competition", "regulatory", "downgrade", "concerns", "challenges"]

    positive_news_count = 0
    negative_news_count = 0
    neutral_or_mixed_news_count = 0

    for headline in news_headlines:
        headline_lower = headline.lower()
        is_positive = any(keyword in headline_lower for keyword in positive_keywords)
        is_negative = any(keyword in headline_lower for keyword in negative_keywords)

        if is_positive and not is_negative:
            positive_news_count += 1
        elif is_negative and not is_positive:
            negative_news_count += 1
        else: # Either both positive and negative, or neither
            neutral_or_mixed_news_count += 1

    if news_headlines:
        analysis_parts.append("\n--- Recent News Sentiment ---")
        total_headlines = len(news_headlines)
        if positive_news_count > negative_news_count and positive_news_count > neutral_or_mixed_news_count:
            analysis_parts.append(f"- The news sentiment is predominantly positive, with {positive_news_count} out of {total_headlines} headlines indicating favorable developments.")
        elif negative_news_count > positive_news_count and negative_news_count > neutral_or_mixed_news_count:
            analysis_parts.append(f"- The news sentiment leans negative, with {negative_news_count} out of {total_headlines} headlines highlighting potential challenges.")
        elif neutral_or_mixed_news_count == total_headlines:
            analysis_parts.append("- The news headlines appear largely neutral or do not contain strong positive/negative indicators.")
        else:
            analysis_parts.append("- The news sentiment is mixed, with a balance of positive, negative, and neutral/mixed reports.")

        analysis_parts.append("\n--- Key Headlines ---")
        if news_headlines:
            # List up to the top 3 headlines for brevity
            for i, headline in enumerate(news_headlines[:3]):
                analysis_parts.append(f"  - {headline}")
        else:
            analysis_parts.append("  No specific news headlines were retrieved.")
    else:
        analysis_parts.append("\nNo recent news headlines available for sentiment analysis.")

    # --- Concluding Remark based on combined sentiment ---
    analysis_parts.append("\n--- Overall Conclusion ---")
    if price_change < -0.5 and negative_news_count > positive_news_count:
        analysis_parts.append(f"The significant decline in {ticker} stock price today appears to be strongly correlated with recent negative news developments.")
    elif price_change > 0.5 and positive_news_count > negative_news_count:
        analysis_parts.append(f"The notable increase in {ticker} stock price today is likely driven by positive news and favorable market sentiment.")
    elif price_change != 0 and (positive_news_count > 0 or negative_news_count > 0):
        analysis_parts.append(f"The current price action for {ticker} is likely influenced by the available news, which presents a {'positive' if positive_news_count > negative_news_count else 'negative'} bias.")
    else:
        analysis_parts.append(f"The current market behavior for {ticker} might be due to broader market trends or factors not captured by the immediate news. Further analysis is recommended.")


    return "\n".join(analysis_parts)