# CryptoTrader

CryptoTrader is a Python-based cryptocurrency trading bot that integrates with the Robinhood Crypto API. It features automated market data retrieval, configurable trading strategies, and a user-friendly GUI for real-time trading and analytics.

## Key Features

- **Robinhood API Integration**:
  - Secure API authentication with API keys and private keys.
  - Market data retrieval (best bid/ask prices) for popular trading pairs (e.g., BTC-USD, ETH-USD).
  - Modular design for extending API interactions, such as placing and managing orders.

- **Customizable Trading Strategies**:
  - Dynamic thresholds for buy/sell signals based on market data.
  - Configurable parameters for lookback period, buy/sell margins, and trade quantity.

- **User Interface**:
  - Interactive GUI built with Tkinter for monitoring real-time market data.
  - Adjustable trading parameters directly from the dashboard.

- **Dry Run Mode**:
  - Test trading strategies without executing real trades.
  - Seamlessly switch to live trading when ready.

## Installation

1.  Clone the repository:
    ```
    git clone https://github.com/yourusername/CryptoTrader.git
    cd CryptoTrader
    ```

2.	Create a virtual environment and install dependencies:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3.  Configure your .env file:
    ```
    API_KEY=your_api_key
    BASE64_PRIVATE_KEY=your_private_key
    LOOKBACK_PERIOD=5400
    BUY_MARGIN=0.02
    SELL_MARGIN=0.02
    TRADE_QUANTITY=0.30
    DRY_RUN=True
    ```

## Installation

1. Activate the virtual environment:
   ```
   source .venv/bin/activate
   ```
2. Run the trading bot:
   ```
   python main.py
   ```
3. Interact with the GUI to monitor prices and adjust trading parameters.

## File Structure

  ```
CryptoTrader/
│
├── main.py               # Main script
├── api_client.py         # Robinhood API client
├── strategies.py         # Trading strategy logic
├── gui.py                # User interface
├── .env                  # Environment variables
└── README.md             # Project documentation
  ```
