import pandas as pd
from typing import List
import re
import math
import time

IMPORT_PATH = 'data/catalog_product_20210403_173129.csv'
OUTPUT_PATH = f'data/shopify_import_{time.strftime("%Y%m%d_%H%M%S")}.csv'

raw_products = pd.read_csv(IMPORT_PATH, low_memory=False)

# Strip useless data
def get_empty_columns(df: pd.DataFrame): 
    empty_columns = []
    
    for col in df:
        value = df[col].unique()
        if value.size == 1:
            empty_columns.append(col)

    return empty_columns

unused_columns = ['_root_category', 'collections', 'msrp_display_actual_price_type', 'msrp_enabled', 'news_from_date', 'news_to_date', 'page_layout', 'special_from_date', 'special_to_date', 'tax_class_id'] + get_empty_columns(raw_products)
magento_products = raw_products.drop(columns=unused_columns)

# Magento Product Utilities
magento_product_index_limit = len(magento_products.index)
num_of_rows = magento_products.shape[0]
def generate_column(input): return [input] * num_of_rows
empty_column = generate_column('')

def backfill_array(input: List[str], empty_val = ''):
    output = [] 
    for index, value in enumerate(input):
        if (value != empty_val):
            output.append(value)
        else:
            cursor = 1
            past_value = input[index - cursor]
            while(past_value == empty_val):
                cursor += 1
                past_value = input[index - cursor]

            output.append(past_value)
    
    return output

# Published column
def to_published(value: int): 
    if value == 1:
        return 'TRUE'
    elif value == 2:
        return 'FALSE'
    else:
        return ''

published_column = list(map(to_published, magento_products['status']))
published_column = backfill_array(published_column)

# Status column
def to_status(value: int): 
    if value == 1:
        return 'active'
    elif value == 2:
        return 'draft'
    else:
        return ''

status_column = list(map(to_status, magento_products['status']))
status_column = backfill_array(status_column)

# Img Src column
def generate_url(ext): 
    img_base = 'https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95'
    if (type(ext) is str):
        return img_base + ext
    else:
        return ''

img_src_column = list(map(generate_url, magento_products['_media_image']))

# Variant Grams
def carats_to_grams(input: str):
    if type(input) is not str:
        return 0

    decimal_regex = r'\d*\.{0,1}\d+'

    try:
        carat_decimal_str = re.search(decimal_regex, input).group()
    except AttributeError:
        carat_decimal_str = ''

    if carat_decimal_str == '':
        return 0

    carat_float = float(carat_decimal_str)
    grams_float = carat_float * 0.2
    grams = math.floor(grams_float)

    return grams

variant_grams_column = list(map(carats_to_grams, magento_products['total_gem_weight']))




# Format to match Shopify CSV import shape
shopify_df = { 
    'Handle': magento_products['url_key'],
    'Title': magento_products['name'],
    'Body (HTML)': magento_products['short_description'],
    'Vendor': empty_column,
    'Type': magento_products['_category'],
    'Tags': empty_column,
    'Published': published_column,
    'Option1 Name': empty_column, # Filled later
    'Option1 Value': empty_column, # Filled later
    'Option2 Name': empty_column, # Filled later
    'Option2 Value': empty_column, # Filled later
    'Option3 Name': empty_column, # Filled later
    'Option3 Value': empty_column, # Filled later
    'Variant SKU': magento_products['sku'],
    'Variant Grams': variant_grams_column, 
    'Variant Inventory Tracker': empty_column,  
    'Variant Inventory Qty': magento_products['qty'],
    'Variant Inventory Policy': generate_column('deny'), 
    'Variant Fulfillment Service': generate_column('manual'),
    'Variant Price': magento_products['price'], 
    'Variant Compare At Price': empty_column, 
    'Variant Requires Shipping': generate_column('TRUE'), 
    'Variant Taxable': generate_column('TRUE'), 
    'Variant Barcode': empty_column,
    'Image Src': img_src_column, 
    'Image Position': empty_column,
    'Image Alt Text': magento_products['_media_lable'], 
    'Gift Card': generate_column('FALSE'),
    'SEO Title': magento_products['meta_title'],
    'SEO Description': magento_products['meta_description'],
    'Variant Weight Unit': generate_column('g'),
    'Status': status_column, 
}

shopify_df = pd.DataFrame(data=shopify_df) 




# Utilities for creating variant rows 
def filter_nan(input: List): return list(filter(lambda v: v==v, input))

def product_index_by_sku(sku: str): 
    mask = magento_products['sku'] == sku
    return magento_products.loc[mask].index[0] 

def get_variants_by_sku(sku: str):
    sku_index: int = product_index_by_sku(sku)

    cursor_index = sku_index + 1
    variant_indexes = [sku_index]

    is_last_row = cursor_index == magento_product_index_limit
    if (is_last_row):
        return magento_products.iloc[variant_indexes]

    next_row = magento_products.iloc[cursor_index]

    while (type(next_row['sku']) is not str):
        variant_indexes.append(cursor_index)
        cursor_index += 1
        next_row = magento_products.iloc[cursor_index]

    return magento_products.iloc[variant_indexes]

def get_option_titles_by_sku(sku: str):
    product_variants = get_variants_by_sku(sku)
    option_titles = product_variants['_custom_option_title'].unique()
    option_titles = filter_nan(option_titles)
    return option_titles

def get_option_values_by_sku(sku: str):
    product_variants = get_variants_by_sku(sku)
    option_titles = get_option_titles_by_sku(sku)
    all_option_values = []

    for title in option_titles:
        title_start_index: int = product_variants.loc[product_variants['_custom_option_title'] == title].index[0]
        
        cursor_index = title_start_index + 1
        value_indexes = [title_start_index]
        
        next_row = magento_products.iloc[cursor_index]
        while (type(next_row['_custom_option_store']) is not str):
            value_indexes.append(cursor_index)
            cursor_index += 1
            next_row = magento_products.iloc[cursor_index]

        option_rows = magento_products.iloc[value_indexes]
        option_values = option_rows['_custom_option_row_title'].unique()
        option_values = filter_nan(option_values)
        all_option_values.append(option_values)

    return all_option_values

def get_product_by_sku(sku: str): 
    return magento_products.loc[magento_products['sku'] == sku]

def get_shopify_product_by_sku(sku: str):
    mask = shopify_df['Variant SKU'] == sku
    df: pd.DataFrame = shopify_df.loc[mask]
    return df.copy()

def create_base_shopify_dict(input: dict):
    row = {}

    for key in list(shopify_df.keys()):        
        row[key] = ''

    for key in list(input.keys()):
        row[key] = input[key]

    row['Variant Inventory Policy'] = 'deny'
    row['Variant Fulfillment Service'] = 'manual'
    row['Variant Requires Shipping'] = 'TRUE'
    row['Variant Taxable'] = 'TRUE'
    row['Variant Weight Unit'] = 'g'

    return row

# Initialize shopify_df_csv_output
final_columns = list(shopify_df.columns)
final_values = []
for column in final_columns:
    final_values.append([])

shopify_df_csv_output = pd.DataFrame(columns=final_columns)

# Populate shopify_df_csv_output with unique sku rows and their variants appended
# Awkward and slow, but nececessary to get options formatted the way shopify wants it
skus = list(shopify_df['Variant SKU'].unique())
skus = filter_nan(skus)
skus = skus[:10]
for sku in skus:
    simple_product = get_shopify_product_by_sku(sku).to_dict('records')[0]
    has_options = len(get_option_titles_by_sku(sku)) > 0
    variant_columns = {
        'Handle': simple_product['Handle'],
        'Variant Grams': simple_product['Variant Grams'],
        'Variant Price': simple_product['Variant Price'],
        'Variant Weight Unit': simple_product['Variant Weight Unit'],
    }

    if (has_options):
        option_titles = get_option_titles_by_sku(sku)
        all_option_values = get_option_values_by_sku(sku)

        for title_index, title in enumerate(option_titles):
            option_values = all_option_values[title_index]

            for value_index, value in enumerate(option_values):
                option_title = f'Option{title_index + 1}'
                title_column = f'{option_title} Name'
                value_column =  f'{option_title} Value'
                new_option = {title_column: title, value_column: value}
                
                first_title = title_index == 0
                first_value = value_index == 0
                
                if (first_title):
                    if (first_value):
                        row = {**simple_product, **new_option}
                        shopify_df_csv_output = shopify_df_csv_output.append(row, ignore_index=True)
                    else:
                        new_option = {value_column: new_option[value_column]}
                        row = {**create_base_shopify_dict(new_option), **variant_columns}
                        shopify_df_csv_output = shopify_df_csv_output.append(row, ignore_index=True)
                else:
                    if (first_value):
                        new_option = new_option
                    else:
                        new_option = {value_column: new_option[value_column]}                   
                    row = {**create_base_shopify_dict(new_option), **variant_columns}
                    shopify_df_csv_output = shopify_df_csv_output.append(row, ignore_index=True)
    else: 
        new_option = {'Option1 Name': 'Title', 'Option1 Value': 'Default Title'}
        row = {**simple_product, **new_option}
        shopify_df_csv_output = shopify_df_csv_output.append(row, ignore_index=True)

                
shopify_df_csv_output.to_csv(OUTPUT_PATH)
