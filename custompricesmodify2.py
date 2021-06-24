import os
import time

import pandas as pd

NOW_DATE_TIME = time.strftime("%Y%m%d_%H%M%S")
CUSTOM_PRICES_IMPORT_PATH = 'data/wholesale-prices-columbiagemhouse-2021-06-12.csv'
custom_prices_df = pd.read_csv(CUSTOM_PRICES_IMPORT_PATH, low_memory=False)

# Transfrom price
def from_retail_to_wholesale(price: float):
    if price >= 0.0 and price <= 1500.0:
        return price / 3.0
    
    if price >= 1500.01 and price <= 5000.0:
        return price / 2.5

    if price >= 5000.01 and price <= 30000.0:
        return price / 2.0

    if price >= 30000.01:
        return price / 1.75


custom_prices_df['Wholesale Price'] = custom_prices_df['Price'].apply(from_retail_to_wholesale)

# Output
OUTPUT_PATH = f'data/wholesale-prices-shopify-{NOW_DATE_TIME}.csv'
custom_prices_df.to_csv(OUTPUT_PATH, index=False)
pwd = os.getcwd()
print(f'INFO - Wholesale Club, Custom Prices import spreadsheet generated at: {pwd}/{OUTPUT_PATH}')
