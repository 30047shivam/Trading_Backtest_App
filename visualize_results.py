import matplotlib.pyplot as plt

def plot_bollinger(df, token):
    plt.figure(figsize=(12, 6))
    plt.plot(df['Close'], label='Close Price')
    plt.plot(df['lower_band'], label='Lower Bollinger Band', linestyle='--')
    plt.plot(df['upper_band'], label='Upper Bollinger Band', linestyle='--')
    plt.title(f"Bollinger Bands for {token}")
    plt.legend()
    plt.show()
