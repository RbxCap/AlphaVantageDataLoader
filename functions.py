import pandas as pd
import requests
from datetime import datetime, timedelta
from tqdm import tqdm
from typing import Optional, List


class OptionsDataFetcher:
    """
    A class to fetch and wrangle options data from Alpha Vantage for a given ticker.
    """
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str):
        """
        Initialize the OptionsDataFetcher.

        :param api_key: API key for Alpha Vantage
        """
        self.api_key = api_key

    def get_workdays(self, start_date: str, end_date: str) -> List[str]:
        """
        Generate a list of workdays (weekdays) between two given dates.

        :param start_date: Start date in 'YYYY-MM-DD' format.
        :param end_date: End date in 'YYYY-MM-DD' format.
        :return: List of workday strings in 'YYYY-MM-DD' format.
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return [(start + timedelta(days=i)).strftime("%Y-%m-%d")
                for i in range((end - start).days + 1) if (start + timedelta(days=i)).weekday() < 5]

    def fetch_options_data(self, ticker: str, start_date: str, end_date: str, option_type: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch historical options data from Alpha Vantage.

        :param ticker: The ticker symbol (e.g., 'AAPL').
        :param start_date: Start date in 'YYYY-MM-DD' format.
        :param end_date: End date in 'YYYY-MM-DD' format.
        :param option_type: Option type ('call' or 'put').
        :return: DataFrame containing historical options data.
        """
        workdays = self.get_workdays(start_date, end_date)
        options_data = pd.DataFrame()

        for date in tqdm(workdays, desc="Fetching Options Data", unit="date"):
            url = f"{self.BASE_URL}?function=HISTORICAL_OPTIONS&date={date}&symbol={ticker}&apikey={self.api_key}"
            response = requests.get(url).json()

            if "Information" in response:
                print(f"API Info: {response['Information']}")
                break

            if response.get("message") == "success":
                daily_data = pd.DataFrame(response["data"])
                daily_data["date"] = date
                options_data = pd.concat([options_data, daily_data], ignore_index=True)

        if option_type:
            options_data = options_data[options_data["type"] == option_type]

        return options_data

    def fetch_stock_prices(self, ticker: str) -> pd.Series:
        """
        Fetch historical stock closing prices from Alpha Vantage.

        :param ticker: The ticker symbol.
        :return: Series with stock close prices indexed by date.
        """
        url = f"{self.BASE_URL}?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={self.api_key}"
        response = requests.get(url).json()
        prices = pd.DataFrame(response["Time Series (Daily)"], dtype=float).T
        prices.index = pd.to_datetime(prices.index)
        return prices["4. close"].sort_index()

    def process_data(self, options_data: pd.DataFrame, stock_prices: pd.Series) -> pd.DataFrame:
        """
        Process options data by merging stock prices and computing additional metrics.

        :param options_data: Raw options data DataFrame.
        :param stock_prices: Series of stock closing prices.
        :return: Processed options data DataFrame.
        """
        options_data["date"] = pd.to_datetime(options_data["date"])
        options_data["option_expiration"] = pd.to_datetime(options_data["expiration"])
        options_data["ttm"] = (options_data["option_expiration"] - options_data["date"]).dt.days

        options_data["stock_price_close"] = options_data["date"].map(lambda d: stock_prices.get(d, None))
        options_data["stock_price_close"] = options_data["stock_price_close"].ffill()

        options_data["option_id"] = options_data.apply(lambda row: f"{row['symbol']}_{row['strike']}_{row['expiration']}", axis=1)
        options_data["selection_date"] = (options_data["date"].dt.dayofweek == 0).astype(int)

        options_data["bid"] = pd.to_numeric(options_data["bid"], errors='coerce')
        options_data["ask"] = pd.to_numeric(options_data["ask"], errors='coerce')
        options_data["mean_price"] = (options_data["bid"] + options_data["ask"]) / 2

        col_names = [
            'strike', 'last', 'mark',
            'bid', 'bid_size', 'ask',
            'ask_size', 'volume', 'open_interest',
            'implied_volatility', 'delta', 'gamma',
            'theta', 'vega', 'rho',
            'ttm', 'stock_price_close', 'mean_price'
        ]

        options_data[col_names] = options_data[col_names].apply(pd.to_numeric, errors="coerce")

        return options_data

    def get_wrangled_options_data(self, ticker: str, start_date: str, end_date: str, option_type: Optional[str] = None) -> pd.DataFrame:
        """
        Fully processed options data including stock prices and additional metrics.

        :param ticker: The ticker symbol.
        :param start_date: Start date in 'YYYY-MM-DD' format.
        :param end_date: End date in 'YYYY-MM-DD' format.
        :param option_type: Option type ('call' or 'put').
        :return: Processed DataFrame with enriched options data.
        """
        options_data = self.fetch_options_data(ticker, start_date, end_date, option_type)
        stock_prices = self.fetch_stock_prices(ticker)

        return self.process_data(options_data, stock_prices)

