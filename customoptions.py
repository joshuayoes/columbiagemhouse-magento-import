import time
from typing import Dict
import pandas as pd

class CustomOptions:
    column_headers = ["Option_unique_name","Option_display_name","Option_tooltip","Option_helptext","Option_type","Option_value","Option_price","Swatch_type","Swatch_value","Character_limit","Minimum_selection","Maximum_selection","Variant_id","Variant_name","Default","One_time_charge","Product_id"]

    def __init__(self):
        row = {}
        for header in self.column_headers:
            row[header] = []

        self.df = pd.DataFrame(data=row)


    def create_base_row(self, input: Dict[str, str]):
        row = {}
        for key in list(self.column_headers):        
            row[key] = ''

        for key in list(input.keys()):
            row[key] = input[key]

            if type(row[key]) is str:
                row[key] = row[key].strip()

        return row


    def add_product_options(self, option_titles, all_option_values, price_map, product_id, variant_id):
        for title_index, title in enumerate(option_titles):
            unique_name = f'{product_id}__{title}'
            display_name = title
            
            for option_index, option_value in enumerate(all_option_values[title_index]):
                first_option = option_index == 0
                option_price = int(price_map[option_value])
                
                row = self.create_base_row({
                    'Option_unique_name': unique_name,
                    'Option_value': option_value,
                    'Option_price': option_price,
                    'Default': 'No',
                })

                if first_option:
                    row['Option_display_name'] =  display_name
                    row['Option_type'] = 'dropdown'
                    row['Default'] = 'Yes'
                    row['Option_tooltip'] = f'Select {display_name}'
                    row['Option_helptext'] = f'Select {display_name}'
                    row['Product_id'] = product_id
                    
                self.df = self.df.append(row, ignore_index=True)


    def to_output(self):
        print(self.df)


    def to_csv(self):
        NOW_DATE_TIME = time.strftime("%Y%m%d_%H%M%S")
        OUTPUT_PATH = f'data/shopify_custom_option_import_{NOW_DATE_TIME}.csv'
        self.df.to_csv(OUTPUT_PATH, index=False)
    
    def to_xlsx(self):
        NOW_DATE_TIME = time.strftime("%Y%m%d_%H%M%S")
        OUTPUT_PATH = f'data/shopify_custom_option_import_{NOW_DATE_TIME}.xlsx'
        self.df.to_excel(OUTPUT_PATH, index=False)