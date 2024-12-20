import os
import tkinter as tk
from dotenv import load_dotenv
from api_client import CryptoAPITrading
from strategies import TradingStrategy
from gui import TradingDashboardGUI

# Load environment variables
load_dotenv()

LOOKBACK_PERIOD = int(os.getenv("LOOKBACK_PERIOD", 5400))
BUY_MARGIN = float(os.getenv("BUY_MARGIN", 0.02))
SELL_MARGIN = float(os.getenv("SELL_MARGIN", 0.02))
TRADE_QUANTITY = float(os.getenv("TRADE_QUANTITY", 0.30))


def main():
    # Determine mode
    is_dry_run = os.getenv("DRY_RUN", "False").lower() == "true"
    mode = "DRY RUN" if is_dry_run else "LIVE"
    print(f"Running in {mode} mode. {'No trades' if is_dry_run else 'Real trades'} will be executed.")

    # Initialize API client
    try:
        api_client = CryptoAPITrading()
    except ValueError as e:
        print(f"Error initializing API client: {e}")
        return

    # Initialize strategies for each coin
    coins = ["AVAX-USD", "XTZ-USD", "DOGE-USD", "BTC-USD", "ETH-USD"]
    strategies = {}
    for coin in coins:
        try:
            strategies[coin] = TradingStrategy(api_client, coin, LOOKBACK_PERIOD)
        except Exception as e:
            print(f"Error initializing strategy for {coin}: {e}")

    # Start the GUI
    root = tk.Tk()
    app = TradingDashboardGUI(root, strategies)
    root.mainloop()


if __name__ == "__main__":
    main()