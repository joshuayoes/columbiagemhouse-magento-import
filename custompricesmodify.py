import os
import time

import pandas as pd

NOW_DATE_TIME = time.strftime("%Y%m%d_%H%M%S")
IMPORT_PATH = 'data/wholesale-prices-columbiagemhouse-2021-06-07.csv'
OUTPUT_PATH = f'data/wholesale-prices-shopify-{NOW_DATE_TIME}.csv'
custom_prices_df = pd.read_csv(IMPORT_PATH, low_memory=False)

# Transfrom price
def to_retail_price(price: float):    
    if price >= 0.0 and price <= 500.0:
        return price * 3.0
    
    if price >= 500.01 and price <= 2000.0:
        return price * 2.5

    if price >= 2000.01 and price <= 15000.0:
        return price * 2.0

    if price >= 15000.01:
        return price * 1.75

    raise Exception('Price is not within a valid range')

custom_prices_df['Wholesale Price'] = custom_prices_df['Price']
custom_prices_df['Price'] = custom_prices_df['Price'].apply(to_retail_price)

# Output
custom_prices_df.to_csv(OUTPUT_PATH, index=False)
pwd = os.getcwd()
print(f'INFO - Wholesale Club, Custom Prices import spreadsheet generated at: {pwd}/{OUTPUT_PATH}')
