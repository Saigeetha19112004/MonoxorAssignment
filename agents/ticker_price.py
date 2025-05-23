import requests
import os

def get_current_stock_price(ticker: str) -> float:
    if not ticker:
        print("Error: Ticker symbol is empty for price fetching.")
        return 0.0

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        print("ALPHA_VANTAGE_API_KEY not found in environment variables.")
        return 0.0

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        if "Error Message" in data:
            print(f"Alpha Vantage API error for {ticker}: {data['Error Message']}")
            return 0.0
        if not data.get("Global Quote"):
            print(f"No 'Global Quote' data found for {ticker} from Alpha Vantage. Response: {data}")
            return 0.0

        current_price_str = data["Global Quote"].get("05. price")
        if current_price_str:
            current_price = float(current_price_str)
            print(f"Current price for {ticker}: ${current_price:.2f}")
            return current_price
        else:
            print(f"Could not find '05. price' in Alpha Vantage response for {ticker}. Response: {data}")
            return 0.0

    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error fetching current price for {ticker}: {e}")
        return 0.0
    except ValueError as e:
        print(f"Error parsing price data for {ticker} (non-numeric price received): {e}")
        return 0.0
    except Exception as e:
        print(f"An unexpected error occurred while fetching price for {ticker}: {e}")
        return 0.0
