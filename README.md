OptionsDataFetcher

Overview

The OptionsDataFetcher class fetches and processes historical options data from Alpha Vantage. It is designed for institutional use and allows users to retrieve options data, stock prices, and compute additional metrics for analysis.

Features

Fetch historical options data for a given ticker and time range

Retrieve historical stock prices

Compute time-to-maturity (TTM) and other derived metrics

Process and clean options data for further analysis

Installation

To use this script, ensure you have the following Python libraries installed:

pip install pandas requests tqdm

Usage

Initializing the Fetcher

from options_data_fetcher import OptionsDataFetcher

api_key = "your_alpha_vantage_api_key"
fetcher = OptionsDataFetcher(api_key)

Fetching Options Data

ticker = "AAPL"
start_date = "2024-01-01"
end_date = "2024-03-01"
option_type = "put"  # or "call"

data = fetcher.fetch_options_data(ticker, start_date, end_date, option_type)
print(data.head())

Fetching Stock Prices

stock_prices = fetcher.fetch_stock_prices(ticker)
print(stock_prices.head())

Processing Options Data

processed_data = fetcher.process_data(data, stock_prices)
print(processed_data.head())

Getting Fully Processed Data

full_data = fetcher.get_wrangled_options_data(ticker, start_date, end_date, option_type)
print(full_data.head())

Class Methods

get_workdays(start_date: str, end_date: str) -> List[str]

Generates a list of workdays (weekdays) between two dates.

fetch_options_data(ticker: str, start_date: str, end_date: str, option_type: Optional[str] = None) -> pd.DataFrame

Fetches historical options data from Alpha Vantage.

fetch_stock_prices(ticker: str) -> pd.Series

Fetches historical stock closing prices from Alpha Vantage.

process_data(options_data: pd.DataFrame, stock_prices: pd.Series) -> pd.DataFrame

Processes options data by merging stock prices and computing additional metrics.

get_wrangled_options_data(ticker: str, start_date: str, end_date: str, option_type: Optional[str] = None) -> pd.DataFrame

Returns fully processed options data with stock prices and enriched metrics.

Notes

Requires an Alpha Vantage API key.

API rate limits apply, so excessive requests may be throttled.

Errors due to missing data are handled by converting non-numeric values to NaN.

License

This project is for educational and research purposes. Ensure compliance with Alpha Vantage's terms of use.

