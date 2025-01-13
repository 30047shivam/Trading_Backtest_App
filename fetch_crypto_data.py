import os
import requests
import pandas as pd

# Create a directory to store the downloaded data
os.makedirs("data", exist_ok=True)

def fetch_binance_data(symbol, interval="1d", limit=365):
    """Fetch historical data for a cryptocurrency from Binance."""
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Convert the data into a Pandas DataFrame
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", 
                                         "close_time", "quote_asset_volume", "trades", 
                                         "taker_base_volume", "taker_quote_volume", "ignore"])
        # Convert timestamp to readable date
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        # Keep only the required columns
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        return df
    else:
        print(f"Failed to fetch data for {symbol}: {response.status_code}")
        return None

# List of cryptocurrencies to fetch data for
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT"]  # Add more symbols as needed

# Fetch and save data for each symbol
for symbol in symbols:
    data = fetch_binance_data(symbol)
    if data is not None:
        data.to_csv(f"data/{symbol}.csv", index=False)
        print(f"Saved data for {symbol}.")
