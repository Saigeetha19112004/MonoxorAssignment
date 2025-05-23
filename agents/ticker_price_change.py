import requests
import os
from datetime import datetime, timedelta

def get_price_change(ticker: str) -> float:
    if not ticker:
        print("Error: Ticker symbol is empty for price change calculation.")
        return 0.0

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        print("ALPHA_VANTAGE_API_KEY not found in environment variables.")
        return 0.0

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=compact&apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        if "Error Message" in data:
            print(f"Alpha Vantage API error for {ticker}: {data['Error Message']}")
            return 0.0
        if not data.get("Time Series (Daily)"):
            print(f"No daily time series data found for {ticker} from Alpha Vantage. Response: {data}")
            return 0.0

        time_series = data["Time Series (Daily)"]
        dates = sorted(time_series.keys(), reverse=True)

        if len(dates) < 2:
            print(f"Not enough historical data ({len(dates)} days) to calculate price change for {ticker}.")
            return 0.0

  
        today_date_str = dates[0]
        yesterday_date_str = dates[1]

        today_data = time_series.get(today_date_str)
        yesterday_data = time_series.get(yesterday_date_str)

        if not today_data or not yesterday_data:
            print(f"Missing data for today ({today_date_str}) or yesterday ({yesterday_date_str}) for {ticker}.")
            return 0.0
        today_close_str = today_data.get("4. close")
        yesterday_close_str = yesterday_data.get("4. close")

        if not today_close_str or not yesterday_close_str:
            print(f"Missing closing price data for today or yesterday for {ticker}.")
            return 0.0

        today_close = float(today_close_str)
        yesterday_close = float(yesterday_close_str)

        if yesterday_close == 0:
            print(f"Yesterday's closing price for {ticker} was zero, cannot calculate percentage change.")
            return 0.0

        price_change_percentage = ((today_close - yesterday_close) / yesterday_close) * 100
        price_change_percentage = round(price_change_percentage, 2)

        print(f"Price change for {ticker}: {price_change_percentage:.2f}% (Today's Close: ${today_close:.2f}, Yesterday's Close: ${yesterday_close:.2f})")
        return price_change_percentage

    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error fetching historical data for {ticker}: {e}")
        return 0.0
    except ValueError as e:
        print(f"Error parsing historical price data for {ticker} (non-numeric price received): {e}")
        return 0.0
    except Exception as e:
        print(f"An unexpected error occurred while fetching price change for {ticker}: {e}")
        return 0.0
