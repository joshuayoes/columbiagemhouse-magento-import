# 3rd party modules
import sys
import pandas as pd
from typing import Dict, List
import re
import math
import time
from itertools import product

# Local modules
from images import is_url_broken
from customoptions import CustomOptions
 
# Logging utilities
script_start_time = time.time()
def to_ms(now: float, start: float): return int((now - start) * 1000)

# Import/output spreadsheet constants
NOW_DATE_TIME = time.strftime("%Y%m%d_%H%M%S")
IMPORT_PATH = 'data/catalog_product_20210403_173129.csv'
OUTPUT_PATH = f'data/shopify_product_import_{NOW_DATE_TIME}.csv'

# Handle Magneto product import CSV
raw_magento_product_csv = pd.read_csv(IMPORT_PATH, low_memory=False)

# Strip useless data
def get_empty_columns(df: pd.DataFrame): 
    empty_columns = []
    
    for col in df:
        value = df[col].unique()
        if value.size == 1:
            empty_columns.append(col)

    return empty_columns

unused_columns = ['_root_category', 'collections', 'msrp_display_actual_price_type', 'msrp_enabled', 'news_from_date', 'news_to_date', 'page_layout', 'special_from_date', 'special_to_date', 'tax_class_id'] + get_empty_columns(raw_magento_product_csv)
magento_products = raw_magento_product_csv.drop(columns=unused_columns)

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

# Generate Shopify dataframe columns

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

print('Generating img_src_column')

# Img Src column
def generate_url(path): 
    img_base = 'https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95'
    
    path_exists = type(path) is str
    if path_exists == False: return ''
    
    url = img_base + path

    if is_url_broken(url) == True:
        return ''

    return url

img_src_column = list(map(generate_url, magento_products['_media_image']))

print('img_src_column generated')

# Variant Grams column
def parse_carats(input: str):
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
    return carat_float

def carats_to_grams(input: str):
    if type(input) is not str:
        return 0

    carat_float = parse_carats(input)
    grams_float = carat_float * 0.2
    grams = math.floor(grams_float)

    return grams

variant_grams_column = list(map(carats_to_grams, magento_products['total_gem_weight']))

# Tags column
tags_column = []

def parse_total_gem_weight(input: str):
    if type(input) is not str:
        return ''

    if re.search('varies', input, re.IGNORECASE):
        return input.strip().title()

    return f'{parse_carats(input)} cw'

print('Generating tags column')
for index, row in magento_products.iterrows():
    tags: List[str] = []
    def add(label: str, input):
        if type(input) is str and input != '':
            tags.append(f"{label}{input.strip()}")

    add('Total Gem Weight: ', parse_total_gem_weight(row["total_gem_weight"]))
    add('Treatment: ', row["treatment"])
    add('Color: ', row["colors"])
    add('Fair Trade Level: ', row["fairtradelevel"])
    add('Location: ', row["location"])
    add('Origin: ', row["origin"])
    add('Gem Type: ', row["species"])
    add('Gem Cut: ', row["stonecut"])
    add('Shape: ', row["stoneshape"])
    add('Sub Shape: ', row["subshape"])
    add('Stone Size: ', row["stonesize"])
    add('Variety: ', row["variety"])

    joined_tags = ', '.join(tags)
    tags_column.append(joined_tags)

print('Tags column generated')

def sanitize_input(input: str, replacement: str):
    if pd.isna(input): return ''

    sanitized = input.replace('\r\n', replacement)
    sanitized = sanitized.replace('\r', replacement)
    sanitized = sanitized.replace('\n', replacement)
    sanitized = sanitized.replace('\t', replacement)
    return sanitized

# Body (HTML) column
def to_body_html_column(input: str):
    return sanitize_input(input, '<br/>')

body_html_column = list(map(to_body_html_column, magento_products['short_description']))

# SEO Description column
def to_seo_description(input: str):
    return sanitize_input(input, '')

seo_description_column = list(map(to_seo_description, magento_products['meta_description']))

# Image Alt Text column
def to_image_alt_text(input: str):
    return sanitize_input(input, '')

image_alt_text_column = list(map(to_image_alt_text, magento_products['_media_lable']))

# Format to match Shopify CSV import shape
shopify_df = { 
    'Handle': magento_products['url_key'],
    'Title': magento_products['name'],
    'Body (HTML)': body_html_column,
    'Vendor': empty_column,
    'Type': magento_products['_category'],
    'Tags': tags_column,
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
    'Image Alt Text': image_alt_text_column,
    'Gift Card': generate_column('FALSE'),
    'SEO Title': magento_products['meta_title'],
    'SEO Description': seo_description_column,
    'Variant Weight Unit': generate_column('g'),
    'Status': status_column, 
    'Collection': magento_products['collection_1'], 
}

shopify_df = pd.DataFrame(data=shopify_df) 
print('shopify_df populated')



# Utilities for creating variant rows 
def filter_nan(input: List): return list(filter(lambda v: v==v, input))

def get_magento_product_index_by_sku(sku: str): 
    mask = magento_products['sku'] == sku
    return magento_products.loc[mask].index[0] 

def get_variants_by_sku(sku: str):
    sku_index: int = get_magento_product_index_by_sku(sku)

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
    option_titles: List[str] = product_variants['_custom_option_title'].unique()
    option_titles = filter_nan(option_titles)
    return option_titles

def get_option_values_by_sku(sku: str):
    product_variants = get_variants_by_sku(sku)
    option_titles = get_option_titles_by_sku(sku)
    all_option_values: List[List[str]] = []

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

def get_option_price_by_sku(sku: str):
    product_variants = get_variants_by_sku(sku)
    option_titles = get_option_titles_by_sku(sku)
    all_option_prices: List[List[float]] = []

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
        option_prices = option_rows['_custom_option_row_price']
        all_option_prices.append(option_prices)

    return all_option_prices

def get_magento_product_by_sku(sku: str): 
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

def calculate_variant_price(base, variant):
    if (pd.isnull(base)):
        base = 0
    
    if (pd.isnull(variant)):
        variant = 0
    
    return int(base) + int(variant)

# Initialize shopify_df_csv_output
final_columns = list(shopify_df.columns)
shopify_df_csv_output = pd.DataFrame(columns=final_columns)

# Initialize Infinite Product Options spreadsheet export
custom_options = CustomOptions()
custom_options_count = 0

# Populate shopify_df_csv_output with unique sku rows and their variants appended
# Awkward and slow, but nececessary to get options formatted the way shopify wants it
skus = list(shopify_df['Variant SKU'].unique())
skus = filter_nan(skus)

include_only_first_10 = ('-s' in sys.argv)
if include_only_first_10 == True:
    skus = skus[:10]

skus_count = len(skus)
for sku_index, sku in enumerate(skus):
    start_time = time.time()
    position = f'{sku_index}/{skus_count}'
    simple_product = get_shopify_product_by_sku(sku).to_dict('records')[0]
    has_options = len(get_option_titles_by_sku(sku)) > 0
    variant_columns = {
        'Handle': simple_product['Handle'],
        'Variant SKU': simple_product['Variant SKU'],
        'Variant Grams': simple_product['Variant Grams'],
        'Variant Weight Unit': simple_product['Variant Weight Unit'],
    }

    if (has_options == False):
        new_option = {'Option1 Name': 'Title', 'Option1 Value': 'Default Title'}
        row = {**simple_product, **new_option}
        shopify_df_csv_output = shopify_df_csv_output.append(row, ignore_index=True)

    if (has_options == True):
        option_titles = get_option_titles_by_sku(sku)
        all_option_values = get_option_values_by_sku(sku)
        all_option_prices = get_option_price_by_sku(sku)

        # Allow for lookup by option_value: {[option_value]: option_price}
        price_map: Dict[str, float] = {}
        for outer_index, option_values in enumerate(all_option_values):
            for inner_index, value in enumerate(option_values):
                price_map[value] = all_option_prices[outer_index].values[inner_index]

        # Create all possible variants, populate with row information
        all_value_combinations = list(product(*all_option_values))

        # Handle products with more than 100 variants
        if len(all_value_combinations) > 100:
            custom_options.add_product_options(option_titles=option_titles, all_option_values=all_option_values, price_map=price_map, product_id=simple_product['Handle'], variant_id=simple_product['Variant SKU'])
            
            custom_new_option = {'Option1 Name': 'Title', 'Option1 Value': 'Default Title'}
            custom_row = {**simple_product, **new_option}
            shopify_df_csv_output = shopify_df_csv_output.append(custom_row, ignore_index=True)
            
            custom_options_count = custom_options_count + 1
            print(f"{position} | {simple_product['Handle']} | {len(all_value_combinations)} variants | {to_ms(time.time(), start_time)} ms")
            continue 

        # Handle products with less than 100 variants
        all_variant_rows: List[dict] = []
        for value_index, value_tuple in enumerate(all_value_combinations):
            row = {}
            row['Variant Price'] = simple_product['Variant Price']
            # Add unique option values
            for option_index, option_value in enumerate(value_tuple):
                n = option_index + 1
                if n > 3: 
                    raise Exception(f'More than 3 values {option_value}')
                
                row[f'Option{n} Value'] = option_value.strip()
                row[f'Option{n} Name'] = ''
                row['Variant Price'] = row['Variant Price'] + price_map[option_value]

            # Populate shared columns            
            is_first_row = value_index == 0
            if is_first_row:
                row = {**simple_product, **row}
            else:
                row = {**variant_columns, **row}
                row = create_base_shopify_dict(row)

            all_variant_rows.append(row)
        
        # Add row titles to first variant
        for index, title in enumerate(option_titles):
            n = index + 1
            if n > 3: 
                raise Exception(f'More than 3 values {option_titles}')

            all_variant_rows[0].update({f'Option{n} Name': title})

        # Add rows to output
        for row in all_variant_rows:
            shopify_df_csv_output = shopify_df_csv_output.append(row, ignore_index=True)

    print(f"{position} | {row['Handle']} | {to_ms(time.time(), start_time)} ms")

def include_index(): return ('-i' in sys.argv)

# Output results to spreadsheet 
shopify_df_csv_output.to_csv(OUTPUT_PATH, index=include_index())
custom_options.to_xlsx()
print(f'Number of customized options: {custom_options_count}')

# Log script timing
script_time_in_total_secs = int(time.time() - script_start_time)
script_time_in_min = int(script_time_in_total_secs / 60)
script_time_in_remaining_secs = script_time_in_total_secs % 60
if (script_time_in_total_secs > 60):
    print(f'Script completed in {script_time_in_min} minutes and {script_time_in_remaining_secs} seconds')
else:
    print(f'Script completed in {script_time_in_total_secs} seconds')
