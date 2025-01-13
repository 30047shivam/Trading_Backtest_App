import os
import requests
import pandas as pd

# Your Alpha Vantage API key
API_KEY = "MOGVUG9YWDYEWYWS"

# Create a directory to store downloaded data
os.makedirs("data", exist_ok=True)

def fetch_stock_data(symbol):
    """Fetch historical stock data from Alpha Vantage."""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",  # Fetch daily adjusted stock data
        "symbol": symbol,  # Stock ticker symbol
        "apikey": API_KEY,  # Your API key
        "outputsize": "compact"  # Use "full" for full historical data
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            print(f"No data found for {symbol}.")
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df.reset_index(inplace=True)
        df.columns = ["timestamp", "open", "high", "low", "close", "adjusted_close", "volume", "dividend", "split"]
        # Keep only necessary columns
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df["timestamp"] = pd.to_datetime(df["timestamp"])  # Convert timestamp to datetime
        return df
    else:
        print(f"Failed to fetch data for {symbol}. Status Code: {response.status_code}")
        return None

# Example: List of stock symbols to fetch
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # Add more symbols if needed

# Fetch and save data for each stock
for symbol in symbols:
    stock_data = fetch_stock_data(symbol)
    if stock_data is not None:
        stock_data.to_csv(f"data/{symbol}.csv", index=False)  # Save as CSV
        print(f"Data for {symbol} saved.")
