import os
import pandas as pd
from ta.volatility import BollingerBands
import numpy as np

class Backtest:
    def __init__(self, data, token_name):
        self.data = data
        self.token_name = token_name
        self.trades = []

    def calculate_bollinger_bands(self):
        bb = BollingerBands(close=self.data["close"], window=20, window_dev=2)
        self.data["bollinger_high"] = bb.bollinger_hband()
        self.data["bollinger_low"] = bb.bollinger_lband()

    def simulate_trades(self):
        for i in range(len(self.data)):
            if self.data["close"][i] < self.data["bollinger_low"][i]:
                buy_price = self.data["close"][i]
                buy_date = self.data["date"][i]
                sell_price = np.nan
                sell_date = None

                for j in range(i + 1, len(self.data)):
                    if self.data["close"][j] > self.data["bollinger_high"][j]:
                        sell_price = self.data["close"][j]
                        sell_date = self.data["date"][j]
                        profit = (sell_price - buy_price) / buy_price * 100

                        self.trades.append({
                            "token": self.token_name,
                            "date_in": buy_date,
                            "buy_price": buy_price,
                            "date_out": sell_date,
                            "sell_price": sell_price,
                            "profit_percentage": profit,
                        })
                        break

    def save_trades(self, file_name="trades.csv", mode="a"):
        trades_df = pd.DataFrame(self.trades)
        if not trades_df.empty:
            trades_df.to_csv(file_name, index=False, mode=mode, header=not os.path.exists(file_name))
            print(f"Trades saved to {file_name}")

# Process all CSV files in the data folder
def process_all_tokens(data_folder, output_file):
    for file_name in os.listdir(data_folder):
        if file_name.endswith(".csv"):
            token_name = file_name.replace(".csv", "")
            print(f"Processing {token_name}...")

            # Load token data
            file_path = os.path.join(data_folder, file_name)
            data = pd.read_csv(file_path)

            # Print the columns to debug
            print(f"Columns in {file_name}: {data.columns.tolist()}")

            # Ensure the 'date' column is in datetime format and handle potential naming issues
            if "date" not in data.columns:
                if "Date" in data.columns:
                    data.rename(columns={"Date": "date"}, inplace=True)
                else:
                    print(f"Warning: 'date' column not found in {file_name}")
                    continue
            data["date"] = pd.to_datetime(data["date"], errors='coerce')

            # Run backtest for the token
            backtest = Backtest(data, token_name)
            backtest.calculate_bollinger_bands()
            backtest.simulate_trades()

            # Save trades to the output file
            backtest.save_trades(file_name=output_file)

# Main entry point
if __name__ == "__main__":
    data_folder = "data"  # Path to your data folder
    output_file = "trades.csv"  # Output file for all trades

    # Process all tokens and generate trades.csv
    process_all_tokens(data_folder, output_file)
    print("All trades processed and saved!")
