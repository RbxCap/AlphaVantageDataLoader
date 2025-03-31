# Wrapper for downloading Data using the AlphaVantage API 
The AlphaVantageDataLoader is a library of methods that can be used to retrieve data via the AlphaVantage API. AlphaVantage offers various types of data and provides a free version with limited access or a paid version. The project is an ongoing task and will be extended step by step.


## Current Features
- ✅ Pulling historical daily option-chains


## Installation
Step-by-step guide to install and set up the project.

```sh
# Clone the repo
git clone https://github.com/RbxCap/AlphaVantageDataLoader.git

# Navigate to the project directory
cd AlphaVantageDataLoader

# Install dependencies
pip install -r requirements.txt

# Run the project
python main.py
```

## Usage  
Data comes from a parquet file or directly via the `OptionsDataFetcher` from the **AlphaVantageDataLoader** project.

```python
from functions import OptionsDataFetcher
from config import api_key

# Example Usage
fetcher = OptionsDataFetcher(api_key)
data = fetcher.get_wrangled_options_data("SPY", "2025-01-01", "2025-03-01", option_type="put")
print(data.head())

```
