import os
import time
from typing import Dict
import pandas as pd

class CustomPrices:
    column_headers = ["Product Type","Product Title","Variant Title","Variant ID","SKU","Price","Compare at Price","Wholesale Price"]

    def __init__(self):
        column = {}
        for header in self.column_headers:
            column[header] = []

        self.df = pd.DataFrame(data=column)


    def create_base_row(self, input: Dict[str, str]):
        row = {}
        for key in list(self.column_headers):        
            row[key] = ''

        for key in list(input.keys()):
            row[key] = input[key]

            if type(row[key]) is str:
                row[key] = row[key].strip()

        return row

    def to_retail_price(self, price: float):
        if (pd.isna(price)):
            return ''

        if type(price) is str:
            return ''
        
        if price >= 0 and price <= 500.0:
            return price * 3.0
        
        if price >= 500.01 and price <= 2000.0:
            return price * 2.5

        if price >= 2000.01 and price <= 15000.0:
            return price * 2.0

        if price >= 15000.01:
            return price * 1.75

        raise Exception('Price is not within a valid range')

    def add_product(self, product_type, product_title, variant_title, product_sku, product_price):
        row = self.create_base_row({
            "Product Type": product_type,
            "Product Title": product_title,
            "Variant Title": variant_title,
            "Variant ID": '',
            "SKU": product_sku,
            "Price": self.to_retail_price(product_price),
            "Compare at Price":'',
            "Wholesale Price": product_price
        })

        self.df = self.df.append(row, ignore_index=True)


    def to_output(self):
        print(self.df)

    def to_csv(self):
        NOW_DATE_TIME = time.strftime("%Y%m%d_%H%M%S")
        OUTPUT_PATH = f'data/shopify_custom_prices_import_{NOW_DATE_TIME}.csv'
        self.df.to_csv(OUTPUT_PATH, index=False)
        pwd = os.getcwd()
        print(f'INFO - Wholesale Club, Custom Prices import spreadsheet generated at: {pwd}/{OUTPUT_PATH}')
    