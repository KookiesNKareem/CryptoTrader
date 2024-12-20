import sqlite3
import time
import numpy as np
from api_client import CryptoAPITrading


import sqlite3
import time
import numpy as np
from api_client import CryptoAPITrading


class TradingStrategy:
    def __init__(self, api_client: CryptoAPITrading, symbol: str, lookback_period: int):
        """
        Initializes a trading strategy for a specific cryptocurrency.
        :param api_client: Instance of CryptoAPITrading to fetch market data.
        :param symbol: Cryptocurrency symbol (e.g., "BTC-USD").
        :param lookback_period: Number of historical data points to consider.
        """
        self.api_client = api_client
        self.symbol = symbol
        self.lookback_period = lookback_period
        self.prices = []

        # Initialize database connection
        self.conn = sqlite3.connect("prices.db")  # Establish connection to SQLite database
        self.cursor = self.conn.cursor()  # Create a cursor for executing SQL commands

        # Load historical prices on initialization
        self.prices = self._load_historical_prices()

    def _load_historical_prices(self):
        """
        Loads historical prices for the cryptocurrency from the database.
        :return: List of historical prices.
        """
        self.cursor.execute(
            "SELECT price FROM prices WHERE coin = ? ORDER BY timestamp DESC LIMIT ?",
            (self.symbol, self.lookback_period),
        )
        return [row[0] for row in self.cursor.fetchall()]

    def fetch_and_update_prices(self):
        """
        Fetches the latest bid, ask, and mid prices for the specified symbol from the Robinhood API.
        :return: Tuple containing bid, ask, and current price (midpoint).
        """
        try:
            response = self.api_client.make_request(
                "GET",
                f"/api/v1/crypto/marketdata/best_bid_ask/",
                query_params=f"?symbol={self.symbol}"
            )
            if not response or "results" not in response or not response["results"]:
                print(f"No results found for symbol {self.symbol}. Response: {response}")
                return None, None, None

            # Extract the result for the current symbol
            result = next((item for item in response["results"] if item["symbol"] == self.symbol), None)
            if not result:
                print(f"Symbol {self.symbol} not found in API response. Response: {response}")
                return None, None, None

            bid = float(result.get("bid_price", 0))  # Default to 0 if missing
            ask = float(result.get("ask_price", 0))  # Default to 0 if missing
            current_price = (bid + ask) / 2 if bid and ask else None  # Handle missing data
            if current_price is None:
                print(f"Invalid bid/ask prices in response for {self.symbol}. Response: {result}")
                return None, None, None

            self._save_price(current_price)
            return bid, ask, current_price
        except Exception as e:
            print(f"Error fetching prices for {self.symbol}: {e}")
            return None, None, None

    def _save_price(self, price):
        """
        Saves the latest price to the database.
        :param price: Latest price.
        """
        self.cursor.execute(
            "INSERT INTO prices (timestamp, coin, price) VALUES (?, ?, ?)",
            (time.time(), self.symbol, price),
        )
        self.conn.commit()
        self.prices.append(price)

        # Maintain only the lookback period size
        if len(self.prices) > self.lookback_period:
            self.prices.pop(0)

    def calculate_thresholds(self):
        """
        Calculates advanced buy and sell thresholds using volatility, EMA, and Bollinger Bands.
        :return: Tuple containing buy and sell thresholds.
        """
        if len(self.prices) < 10:
            return 0, 0  # Insufficient data to calculate thresholds

        # Parameters
        ema_alpha = 0.2  # Smoothing factor for EMA
        z_score = 1.96  # 95% confidence interval

        # Calculate EMA
        ema = self._calculate_ema(self.prices, alpha=ema_alpha)

        # Calculate standard deviation (volatility)
        volatility = np.std(self.prices)

        # Calculate Bollinger Bands
        upper_band = ema + (2 * volatility)
        lower_band = ema - (2 * volatility)

        # Use confidence interval to adjust thresholds
        mean_price = np.mean(self.prices)
        margin_of_error = z_score * (volatility / np.sqrt(len(self.prices)))
        buy_threshold = mean_price - margin_of_error
        sell_threshold = mean_price + margin_of_error

        # Take the stricter of Bollinger Band and confidence thresholds
        buy_threshold = max(lower_band, buy_threshold)
        sell_threshold = min(upper_band, sell_threshold)

        return buy_threshold, sell_threshold

    def _calculate_ema(self, prices, alpha=0.2):
        """
        Calculates the Exponential Moving Average (EMA) of a price series.
        :param prices: List of historical prices.
        :param alpha: Smoothing factor (0 < alpha <= 1).
        :return: EMA value.
        """
        ema = prices[0]
        for price in prices[1:]:
            ema = alpha * price + (1 - alpha) * ema
        return ema