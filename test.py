from dotenv import load_dotenv
import os
from api_client import CryptoAPITrading

# Load environment variables from .env file
load_dotenv()

# Debugging: Print the variables to confirm they're loaded
print("API_KEY:", os.getenv("API_KEY"))
print("BASE64_PRIVATE_KEY:", os.getenv("BASE64_PRIVATE_KEY"))

# Initialize the API client
api_client = CryptoAPITrading()
try:
    api_client = CryptoAPITrading()
    api_client.test_api_credentials()
except ValueError as e:
    print(f"Error initializing API client: {e}")
