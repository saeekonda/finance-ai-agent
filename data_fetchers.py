import requests
import pandas as pd # Although not strictly needed for basic fetching, good to include for future data handling
from config import ALPHA_VANTAGE_API_KEY, NEWS_API_KEY # FMP_API_KEY is removed
from yfinance_data_handler import YFinanceDataHandler # Changed to absolute import for direct execution

class FinancialDataFetcher:
    def __init__(self):
        self.alpha_vantage_api_key = ALPHA_VANTAGE_API_KEY
        # self.fmp_api_key = FMP_API_KEY # Removed as FMP is no longer used for Indian stocks

        # Initialize the YFinance handler
        self.yfinance_handler = YFinanceDataHandler()

    def _make_request(self, url, params=None):
        """Helper method to make an HTTP GET request and handle common errors."""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e} - Response: {e.response.text}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request error occurred: {e}")
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
        return None

    def get_us_stock_price(self, symbol):
        """Fetches the current price of a US stock using Alpha Vantage."""
        if not self.alpha_vantage_api_key:
            print("Alpha Vantage API key not set. Cannot fetch US stock price.")
            return None

        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.alpha_vantage_api_key}"
        data = self._make_request(url)

        if data and "Global Quote" in data:
            try:
                price = float(data["Global Quote"]["05. price"])
                return price
            except (KeyError, ValueError):
                print(f"Error parsing Alpha Vantage data for {symbol}. Response: {data}")
                return None
        elif data and "Error Message" in data:
            print(f"Alpha Vantage Error for {symbol}: {data['Error Message']}")
        elif data:
            print(f"Unexpected Alpha Vantage response for {symbol}: {data}")
        return None

    def get_indian_stock_price(self, symbol):
        """
        Fetches the current price of an Indian stock using yfinance.
        Args:
            symbol (str): The stock ticker symbol for NSE (e.g., "RELIANCE.NS").
        Returns:
            float: Current price or None if not found/error.
        """
        return self.yfinance_handler.fetch_current_price(symbol)

    def get_indian_stock_historical_data(self, symbol, start_date=None, end_date=None, period="1mo", interval="1d"):
        """
        Fetches historical data for an Indian stock using yfinance.
        Args:
            symbol (str): The stock ticker symbol for NSE (e.g., "RELIANCE.NS").
            start_date (str): Start date in "YYYY-MM-DD" format.
            end_date (str): End date in "YYYY-MM-DD" format.
            period (str): Valid periods: "1d", "5d", "1mo", etc.
            interval (str): Valid intervals: "1m", "1d", etc.
        Returns:
            pandas.DataFrame: Historical data or None.
        """
        return self.yfinance_handler.fetch_historical_data(symbol, start_date, end_date, period, interval)

    def get_crypto_price(self, crypto_id, vs_currency="usd"):
        """Fetches the current price of a cryptocurrency using CoinGecko."""
        # crypto_id examples: "bitcoin", "ethereum", "ripple"
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={vs_currency}"
        data = self._make_request(url)

        if data and crypto_id in data and vs_currency in data[crypto_id]:
            try:
                price = float(data[crypto_id][vs_currency])
                return price
            except (KeyError, ValueError):
                print(f"Error parsing CoinGecko data for {crypto_id}. Response: {data}")
                return None
        elif data:
            print(f"Could not find price for {crypto_id} in {vs_currency} from CoinGecko. Response: {data}")
        return None


class NewsFetcher:
    def __init__(self):
        self.news_api_key = NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/"

    def _make_request(self, url, params=None):
        """Helper method to make an HTTP GET request and handle common errors."""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e} - Response: {e.response.text}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request error occurred: {e}")
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
        return None

    def get_financial_news(self, query="stocks OR finance OR cryptocurrency", language="en", page_size=5, sort_by="publishedAt"):
        """
        Fetches financial news articles using News API.
        Query can be a company name, stock symbol, or broad financial terms.
        """
        if not self.news_api_key:
            print("News API key not set. Cannot fetch news.")
            return []

        endpoint = "everything"
        params = {
            "q": query,
            "language": language,
            "pageSize": page_size,
            "sortBy": sort_by,
            "apiKey": self.news_api_key
        }
        url = f"{self.base_url}{endpoint}"
        data = self._make_request(url, params=params)

        if data and data.get("status") == "ok":
            return data.get("articles", [])
        elif data:
            print(f"News API Error: {data.get('message', 'Unknown error')}")
        return []

# --- Test Block (Run this directly to test fetchers) ---
if __name__ == "__main__":
    print("--- Testing Data Fetchers ---")

    financial_fetcher = FinancialDataFetcher()

    # Test US Stock Price
    aapl_price = financial_fetcher.get_us_stock_price("AAPL")
    if aapl_price:
        print(f"AAPL Price: ${aapl_price:.2f}")

    # Test Indian Stock Price using yfinance (Use a real Indian symbol like RELIANCE.NS or TCS.NS)
    reliance_price = financial_fetcher.get_indian_stock_price("RELIANCE.NS")
    if reliance_price:
        print(f"RELIANCE.NS Current Price: ₹{reliance_price:.2f}")

    # Test Indian Stock Historical Data using yfinance
    print("\n--- Fetching historical data for TCS.NS (last 1 month) ---")
    tcs_hist = financial_fetcher.get_indian_stock_historical_data("TCS.NS", period="1mo")
    if tcs_hist is not None:
        print(tcs_hist.head())

    # Test Crypto Price
    btc_price = financial_fetcher.get_crypto_price("bitcoin", "usd")
    if btc_price:
        print(f"Bitcoin Price: ${btc_price:.2f}")

    print("\n--- Testing News Fetcher ---")
    news_fetcher = NewsFetcher()
    tech_news = news_fetcher.get_financial_news(query="Microsoft OR Apple", page_size=3)
    if tech_news:
        for i, article in enumerate(tech_news):
            print(f"Article {i+1}: {article.get('title')}")
            print(f"  Source: {article.get('source', {}).get('name')}")
            print(f"  URL: {article.get('url')}\n")
    else:
        print("No news fetched.")