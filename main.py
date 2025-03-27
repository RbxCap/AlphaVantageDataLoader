from functions import OptionsDataFetcher
from config import api_key

# Example Usage
fetcher = OptionsDataFetcher(api_key)
data = fetcher.get_wrangled_options_data("SPY", "2024-01-01", "2024-03-01", option_type="put")
print(data.head())
