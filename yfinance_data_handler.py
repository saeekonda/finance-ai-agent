import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class YFinanceDataHandler:
    def __init__(self):
        print("YFinanceDataHandler initialized.")

    def fetch_historical_data(self, ticker_symbol, start_date=None, end_date=None, period="1mo", interval="1d"):
        """
        Fetches historical data for a given ticker symbol.
        Args:
            ticker_symbol (str): The stock ticker symbol (e.g., "RELIANCE.NS").
            start_date (str): Start date in "YYYY-MM-DD" format.
            end_date (str): End date in "YYYY-MM-DD" format.
            period (str): Valid periods: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max".
            interval (str): Valid intervals: "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo".
                              Intraday data (intervals < 1d) only available for period <= 60 days.
        Returns:
            pandas.DataFrame: Historical data or None if an error occurs.
        """
        try:
            ticker = yf.Ticker(ticker_symbol)
            if start_date and end_date:
                hist_data = ticker.history(start=start_date, end=end_date, interval=interval)
            else:
                hist_data = ticker.history(period=period, interval=interval)

            if hist_data.empty:
                print(f"No historical data found for {ticker_symbol} with specified parameters.")
                return None
            return hist_data
        except Exception as e:
            print(f"Error fetching historical data for {ticker_symbol}: {e}")
            return None

    def fetch_current_price(self, ticker_symbol):
        """
        Fetches the current market price for a given ticker symbol.
        Args:
            ticker_symbol (str): The stock ticker symbol (e.g., "RELIANCE.NS").
        Returns:
            float: Current price or None if not found/error.
        """
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            current_price = info.get('regularMarketPrice')
            if current_price:
                return current_price
            else:
                print(f"Could not retrieve current price for {ticker_symbol}. Info: {info}")
                return None
        except Exception as e:
            print(f"Error fetching current price for {ticker_symbol}: {e}")
            return None

if __name__ == "__main__":
    # Example Usage:
    yfinance_handler = YFinanceDataHandler()

    # Fetch historical data for RELIANCE for the last 1 month
    print("\n--- Fetching 1-month historical data for RELIANCE.NS ---")
    reliance_hist = yfinance_handler.fetch_historical_data("RELIANCE.NS", period="1mo")
    if reliance_hist is not None:
        print(reliance_hist.head())

    # Fetch historical data for TATAMOTORS between specific dates
    print("\n--- Fetching historical data for TATAMOTORS.NS (specific dates) ---")
    tata_motors_hist = yfinance_handler.fetch_historical_data(
        "TATAMOTORS.NS", start_date="2024-01-01", end_date="2024-03-31"
    )
    if tata_motors_hist is not None:
        print(tata_motors_hist.tail())

    # Fetch current price for INFOSYS
    print("\n--- Fetching current price for INFY.NS ---")
    infosys_price = yfinance_handler.fetch_current_price("INFY.NS")
    if infosys_price is not None:
        print(f"Current price of INFY.NS: {infosys_price}")
    else:
        print("Failed to get INFY.NS price.")

    print("\n--- YFinance examples complete ---")