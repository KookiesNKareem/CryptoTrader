import base64
import requests
from nacl.signing import SigningKey
from datetime import datetime, timezone
import os
from typing import Optional, Any
import json
from dotenv import load_dotenv


load_dotenv()
class CryptoAPITrading:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.private_key = os.getenv("BASE64_PRIVATE_KEY")

        if not self.api_key or not self.private_key:
            raise ValueError("API_KEY and BASE64_PRIVATE_KEY must be set in the .env file.")

        self.private_key = SigningKey(base64.b64decode(self.private_key))
        self.base_url = "https://trading.robinhood.com"

    @staticmethod
    def _get_current_timestamp() -> int:
        """
        Gets the current UTC timestamp.
        :return: Integer timestamp.
        """
        return int(datetime.now(timezone.utc).timestamp())

    def get_query_params(self, key: str, *args: Optional[str]) -> str:
        """
        Builds query parameters for the request.
        :param key: Query parameter key.
        :param args: Values for the key.
        :return: Query string.
        """
        if not args:
            return ""

        params = [f"{key}={arg}" for arg in args]
        return "?" + "&".join(params)

    def make_request(self, method: str, path: str, body: str = "", query_params: str = "") -> Any:
        """
        Sends a request to the API.
        """
        url = self.base_url + path + query_params
        headers = self.get_authorization_header(method, path, body, self._get_current_timestamp())

        try:
            response = requests.request(
                method=method, url=url, headers=headers, json=json.loads(body) if body else None, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return None

    def get_authorization_header(self, method: str, path: str, body: str, timestamp: int) -> dict:
        """
        Generates the authorization headers required for the API.
        """
        message_to_sign = f"{self.api_key}{timestamp}{path}{method}{body}"
        signed = self.private_key.sign(message_to_sign.encode("utf-8"))
        return {
            "x-api-key": self.api_key,
            "x-signature": base64.b64encode(signed.signature).decode("utf-8"),
            "x-timestamp": str(timestamp),
        }

    def get_best_bid_ask(self, symbol: str) -> Any:
        """
        Fetches the best bid and ask price for a given symbol.
        :param symbol: Trading pair symbol (e.g., BTC-USD).
        :return: Best bid and ask price data.
        """
        query_params = self.get_query_params("symbol", symbol)
        path = "/api/v1/crypto/marketdata/best_bid_ask/"
        return self.make_request("GET", path, query_params=query_params)
