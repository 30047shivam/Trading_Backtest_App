from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    # File path
    file_path = "C:/Users/mishr/OneDrive/Documents/Trading_Backtest_Assignment/data/trades.csv"
    
    # Generate file if it doesn't exist or add more data
    if not os.path.exists(file_path):
        # Initial data
        data = [
            {"trade_id": 1, "symbol": "AAPL", "quantity": 10, "price": 150},
            {"trade_id": 2, "symbol": "GOOGL", "quantity": 5, "price": 2800},
            {"trade_id": 3, "symbol": "MSFT", "quantity": 8, "price": 300},
        ]
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print("trades.csv generated!")
    else:
        # If file exists, add more data
        new_data = [
            {"trade_id": 4, "symbol": "TSLA", "quantity": 15, "price": 700},
            {"trade_id": 5, "symbol": "AMZN", "quantity": 3, "price": 3300},
            {"trade_id": 6, "symbol": "NFLX", "quantity": 7, "price": 500},
        ]
        df_existing = pd.read_csv(file_path)
        df_new = pd.DataFrame(new_data)
        # Avoid duplicate rows
        df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["trade_id"])
        df_combined.to_csv(file_path, index=False)
        print("More data added to trades.csv!")
    
    # Read and display CSV
    trades = pd.read_csv(file_path)
    return trades.to_html(classes='table table-bordered')

if __name__ == "__main__":
    app.run(debug=True)
