# 3rd party modules
import sys
import os
import pandas as pd
from typing import Dict, List, Union
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

def pretty_print(*args):
    columns: List[str] = []
    for column in args:
        content: str = column['content']
        length: int = column['length']

        columns.append(content.ljust(length))

    print(' | '.join(columns))

def print_info(message: str):
    print(f'INFO - {message}')

# Import/output spreadsheet constants
NOW_DATE_TIME = time.strftime("%Y%m%d_%H%M%S")
IMPORT_PATH = 'data/catalog_product_20210403_173129.csv'
OUTPUT_PATH = f'data/shopify_product_import_{NOW_DATE_TIME}.csv'

print_info('Generating Magneto import csv dataframe')

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

print_info('Generating Shopify dataframe columns')

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
def generate_url(path): 
    img_base = 'https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95'
    
    path_exists = type(path) is str
    if path_exists == False: return ''
    
    url = img_base + path

    if is_url_broken(url) == True:
        return ''

    return url

img_src_column = list(map(generate_url, magento_products['_media_image']))

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

print_info('Generating tags column (slow)')
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
def to_image_alt_text(label: Union[str, None], path: Union[str, None]):
    if type(path) is not str: return ''
    if type(label) is not str: return ''

    img_url = generate_url(path)
    if img_url == '': return ''

    return sanitize_input(label, '')

image_alt_text_column = magento_products[['_media_lable', '_media_image']].apply(lambda x: to_image_alt_text(x._media_lable, x._media_image), axis=1)

# Handles Column
def to_handles(handle: Union[str, None], title: Union[str, None], sku: Union[str, None]):
    if pd.isna(handle) == True: return ''
    if pd.isna(title) == True: return ''
    if pd.isna(sku) == True: return ''

    # Line 6095-6096
    if title == '5x3mm Oval Natural Oregon Sunstone':
        return '5x3mm-oval-natural-oregon-sunstone'
    if title == '1.5mm Round Orange Zircon Melee':
        return '1-5-round-orange-zircon-melee'
    
    # Line 7524-7529
    if sku == 'E034-08401-U1_Nat':
        return '1ct-natural-pastel-montana-sapphire-geocutstm-nat'
    if sku == 'E034-08401-U1_Nat-Light':
        return '1ct-natural-pastel-montana-sapphire-geocutstm-nat-light'
    if sku == 'E034-08401-U1_Nat-Medium':
        return '1ct-natural-pastel-montana-sapphire-geocutstm-nat-medium'
    if sku == 'E034-08401-U1_Nat-Dark':
        return '1ct-natural-pastel-montana-sapphire-geocutstm-nat-dark'
    if sku == 'E034-08401-U1_Nat--Included':
        return '1ct-natural-pastel-montana-sapphire-geocutstm-nat-included'
    if sku == 'E034-08401-U1_Nat-Minor Inclusions':
        return '1ct-natural-pastel-montana-sapphire-geocutstm-nat-minor-inclusions'
    
    # Line 7530-7533
    if sku == 'E034-00304-NAT':
        return '4x2-natural-untreated-pastel-montana-sapphire-baguettes-nat'
    if sku == 'E034-00304-NAT-Light':
        return '4x2-natural-untreated-pastel-montana-sapphire-baguettes-nat-light'
    if sku == 'E034-00304-NAT-Medium':
        return '4x2-natural-untreated-pastel-montana-sapphire-baguettes-nat-medium'
    if sku == 'E034-00304-NAT-Dark':
        return '4x2-natural-untreated-pastel-montana-sapphire-baguettes-nat-dark'
    
    # Line 7534-7537
    if sku == 'E034-00303-NAT':
        return '5x2-5mm-natural-untreated-pastel-montana-sapphire-baguettes-nat'
    if sku == 'E034-00303-NAT-Light':
        return '5x2-5mm-natural-untreated-pastel-montana-sapphire-baguettes-nat-light'
    if sku == 'E034-00303-NAT-Medium':
        return '5x2-5mm-natural-untreated-pastel-montana-sapphire-baguettes-nat-medium'
    if sku == 'E034-00303-NAT-Dark':
        return '5x2-5mm-natural-untreated-pastel-montana-sapphire-baguettes-nat-dark'
    
    # Line 7788-7789
    if sku == 'E034-11940-Fancy':
        return '4mm-hexagonal-rose-cut-fancy-montana-sapphires'
    if sku == 'E034-11944-Fancy':
        return '4-5m-hexagonal-rose-cut-fancy-montana-sapphires'

    # Line 9586-9587
    if title == '8x6mm Oval Cabochon Cut Oregon Chocolate Agate':
        return '8x6mm-oval-cabochon-cut-oregon-chocolate-agate'
    
    # Line 9756-9760
    if sku == 'E034-01635-1':
        return '3-5mm-hexagonal-cut-montana-sapphires'
    if sku == 'E034-01635-LtBlue':
        return '3-5mm-hexagonal-cut-montana-sapphires-ltblue'
    if sku == 'E034-01635-MedBlue':
        return '3-5mm-hexagonal-cut-montana-sapphires-medblue'
    if sku == 'E034-01635-FineBlue':
        return '3-5mm-hexagonal-cut-montana-sapphires-fineblue'
    if sku == 'E034-01635-Teal':
        return '3-5mm-hexagonal-cut-montana-sapphires-teal'
    
    # Line 9761-9765
    if sku == 'E034-01645-1':
        return '4-5mm-hexagonal-cut-montana-sapphires'
    if sku == 'E034-01645-LtBlue':
        return '4-5mm-hexagonal-cut-montana-sapphires-ltblue'
    if sku == 'E034-01645-MedBlue':
        return '4-5mm-hexagonal-cut-montana-sapphires-medblue'
    if sku == 'E034-01645-FineBlue':
        return '4-5mm-hexagonal-cut-montana-sapphires-fineblue'
    if sku == 'E034-01645-Teal':
        return '4-5mm-hexagonal-cut-montana-sapphires-teal'
    
    # Line 9761-9765
    if sku == 'E034-01650-1':
        return '5mm-hexagonal-cut-montana-sapphires'
    if sku == 'E034-01650-MedBlue':
        return '5mm-hexagonal-cut-montana-sapphires-medblue'
    if sku == 'E034-01650-FineBlue':
        return '5mm-hexagonal-cut-montana-sapphires-fineblue'
    if sku == 'E034-01650-Teal':
        return '5mm-hexagonal-cut-montana-sapphires-teal'

    # Line 9754-9758
    if sku == 'E034-01640-1':
        return '4mm-hexagonal-cut-montana-sapphires'
    if sku == 'E034-01640-LtBlue':
        return '4mm-hexagonal-cut-montana-sapphires-ltblue'
    if sku == 'E034-01640-MedBlue':
        return '4mm-hexagonal-cut-montana-sapphires-medblue'
    if sku == 'E034-01640-FineBlue':
        return '4mm-hexagonal-cut-montana-sapphires-fineblue'
    if sku == 'E034-01640-Teal':
        return '4mm-hexagonal-cut-montana-sapphires-teal'

    return handle


handles_column = magento_products[['url_key', 'name', 'sku']].apply(
    lambda x: to_handles(x.url_key, x._values[1], x.sku), axis=1
)

# Format to match Shopify CSV import shape
shopify_df = { 
    'Handle': handles_column,
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
print_info('Shopify dataframe populated')


def filter_longest(x):
    if pd.isna(x):
        return 0

    return len(x)

longest_handle = shopify_df['Handle'].map(filter_longest).max()

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
        last_variants: pd.DataFrame = magento_products.iloc[variant_indexes]
        return last_variants

    next_row = magento_products.iloc[cursor_index]

    while (type(next_row['sku']) is not str):
        variant_indexes.append(cursor_index)
        cursor_index += 1
        next_row = magento_products.iloc[cursor_index]

    all_variants: pd.DataFrame = magento_products.iloc[variant_indexes]
    return all_variants

def get_child_product_option_titles_by_sku(sku: str, child_products: pd.DataFrame):
    titles = child_products['_super_attribute_code'].unique()
    titles: List[str] = filter_nan(titles)

    return titles

def get_option_titles_by_sku(sku: str, product_variants: pd.DataFrame):
    option_titles: List[str] = product_variants['_custom_option_title'].unique()
    option_titles = filter_nan(option_titles)

    parent_product = magento_products.iloc[get_magento_product_index_by_sku(sku)]
    if parent_product['_type'] == 'configurable':
        child_titles = get_child_product_option_titles_by_sku(sku, product_variants)
        option_titles  = option_titles + child_titles

    return option_titles

def get_option_values_by_sku(sku: str, product_variants: pd.DataFrame):
    option_titles = get_option_titles_by_sku(sku, product_variants)
    all_option_values: List[List[str]] = []

    title_key = '_custom_option_title'
    value_key = '_custom_option_row_title'
    cursor_key = '_custom_option_store'

    simple_or_configurable = product_variants.head()['_type']._values[0]
    if simple_or_configurable == 'configurable':
        title_key = '_super_attribute_code'
        value_key = '_super_attribute_option'
        cursor_key = 'sku'
    
    for title in option_titles:
        title_start_index: int = product_variants.loc[product_variants[title_key] == title].index[0]
        
        cursor_index = title_start_index + 1
        value_indexes = [title_start_index]
        
        next_row = magento_products.iloc[cursor_index]
        while (type(next_row[cursor_key]) is not str):
            value_indexes.append(cursor_index)
            cursor_index += 1
            next_row = magento_products.iloc[cursor_index]

        option_rows = magento_products.iloc[value_indexes]
        option_values = option_rows[value_key].unique()
        option_values = filter_nan(option_values)
        all_option_values.append(option_values)

    return all_option_values

def get_option_price_by_sku(sku: str, product_variants: pd.DataFrame):
    option_titles = get_option_titles_by_sku(sku, product_variants)
    all_option_prices: List[List[float]] = []

    base_price = float(product_variants.head()['price']._values[0])

    title_key = '_custom_option_title'
    price_key = '_custom_option_row_price'
    cursor_key = '_custom_option_store'

    simple_or_configurable = product_variants.head()['_type']._values[0]
    if simple_or_configurable == 'configurable':
        title_key = '_super_attribute_code'
        price_key = '_super_attribute_price_corr'
        cursor_key = 'sku'

    for title in option_titles:
        title_start_index: int = product_variants.loc[product_variants[title_key] == title].index[0]
        
        cursor_index = title_start_index + 1
        value_indexes = [title_start_index]
        
        next_row = magento_products.iloc[cursor_index]
        while (type(next_row[cursor_key]) is not str):
            value_indexes.append(cursor_index)
            cursor_index += 1
            next_row = magento_products.iloc[cursor_index]

        option_rows: pd.DataFrame = magento_products.iloc[value_indexes]
        option_prices = option_rows[price_key]

        if simple_or_configurable == 'configurable':
            def normalize_price(_percentage: str):
                if pd.isna(_percentage): return 0

                percentage = re.search(r'[\d\.]+', _percentage).group()
                ratio_decimal = float(percentage) / 100
                additional_cost = base_price * ratio_decimal

                return round(additional_cost, 2)

            option_prices = option_prices.apply(normalize_price)

        all_option_prices.append(option_prices)

    return all_option_prices

def get_child_product_variant_sku_by_value(parent_sku: str, value: str, product_variants: pd.DataFrame):
    simple_or_configurable = product_variants.head()['_type']._values[0]
    if simple_or_configurable == 'simple':
        return ''
    
    title_key = '_super_attribute_code'
    cursor_key = 'sku'
    sku_key = '_super_products_sku'
    value_key = '_super_attribute_option'

    child_product_sku: str = ''

    option_titles = get_option_titles_by_sku(parent_sku, product_variants)
    for title in option_titles:
        title_start_index: int = product_variants.loc[product_variants[title_key] == title].index[0]
        
        cursor_index = title_start_index + 1
        value_indexes = [title_start_index]
        
        next_row = magento_products.iloc[cursor_index]
        while (type(next_row[cursor_key]) is not str):
            value_indexes.append(cursor_index)
            cursor_index += 1
            next_row = magento_products.iloc[cursor_index]

        option_rows: pd.DataFrame = magento_products.iloc[value_indexes]
        option_sku = option_rows.loc[option_rows[value_key] == value]
        option_sku = option_sku[sku_key]._values[0]

        if pd.isna(option_sku) == False:
            child_product_sku = option_sku
            break

    return child_product_sku 
    
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
skus_count = len(skus)

# Smaller ranges to import Custom Options
# [:1000]
# [1000:1250]
# [1250:1300]
# [1300:1500]
# [1500:2500]
# [2500:4000]
# [4000:]

include_only_first_10 = ('-s' in sys.argv)
if include_only_first_10 == True:
    skus = skus[0:10]

# Logging utilites
def print_simple_product(position, handle, time):
    pretty_print(
        {'content': position, 'length': len(f'{skus_count}/{skus_count}')},
        {'content': handle, 'length': longest_handle},
        {'content': time, 'length': len('1000 ms')},
    )
    
def print_variant_product(position, handle, time, variant_count):
    pretty_print(
        {'content': position, 'length': len(f'{skus_count}/{skus_count}')},
        {'content': handle, 'length': longest_handle},
        {'content': time, 'length': len('1000 ms')},
        {'content': variant_count, 'length': len('1000 variants')},
    )

print_info('Begin to generate final spreadsheets for product import by SKU value...')

SKUS_TO_SKIP = ['371-09195-1', '9565-']

for sku_index, sku in enumerate(skus):
    start_time = time.time()
    position = f'{sku_index}/{skus_count}'
    simple_product = get_shopify_product_by_sku(sku).to_dict('records')[0]
    product_variants = get_variants_by_sku(sku)
    has_options = len(get_option_titles_by_sku(sku, product_variants)) > 0 
    variant_columns = {
        'Handle': simple_product['Handle'],
        'Variant SKU': simple_product['Variant SKU'],
        'Variant Grams': simple_product['Variant Grams'],
        'Variant Weight Unit': simple_product['Variant Weight Unit'],
    }

    if sku in SKUS_TO_SKIP:
        continue

    if (has_options == False):
        new_option = {'Option1 Name': 'Title', 'Option1 Value': 'Default Title'}
        row = {**simple_product, **new_option}
        shopify_df_csv_output = shopify_df_csv_output.append(row, ignore_index=True)

    if (has_options == True):
        option_titles = get_option_titles_by_sku(sku, product_variants)
        all_option_values = get_option_values_by_sku(sku, product_variants)
        all_option_prices = get_option_price_by_sku(sku, product_variants)

        # Allow for lookup by option_value: {[option_value]: option_price}
        price_map: Dict[str, float] = {}
        for outer_index, option_values in enumerate(all_option_values):
            for inner_index, value in enumerate(option_values):
                price_map[value] = all_option_prices[outer_index].values[inner_index]

        # Create all possible variants, populate with row information
        all_value_combinations = list(product(*all_option_values))

        # Handle products with more than 100 variants
        if len(all_value_combinations) > 100:
            custom_options.add_product_options(
                option_titles=option_titles, 
                all_option_values=all_option_values, 
                price_map=price_map, 
                product_id=simple_product['Handle'], 
                variant_id=simple_product['Variant SKU']
            )
            
            custom_new_option = {'Option1 Name': 'Title', 'Option1 Value': 'Default Title'}
            custom_row = {**simple_product, **custom_new_option}
            custom_row['Tags'] += ', Options Managed By Infinite Product Options'
            shopify_df_csv_output = shopify_df_csv_output.append(custom_row, ignore_index=True)
            
            custom_options_count = custom_options_count + 1

            variant_execution_time = to_ms(time.time(), start_time)
            print_variant_product(position, simple_product['Handle'], f'{variant_execution_time} ms', f'{len(all_value_combinations)} variants')
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
                
                variant_sku = get_child_product_variant_sku_by_value(sku, option_value, product_variants)

                if variant_sku != '':
                    row['Variant SKU'] = variant_sku


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

            if title == 'stonesize':
                title = 'Stone Size'
            
            if title == 'colors':
                title = 'Colors'

            all_variant_rows[0].update({f'Option{n} Name': title})

        # Add rows to output
        for row in all_variant_rows:
            shopify_df_csv_output = shopify_df_csv_output.append(row, ignore_index=True)

    execution_time = to_ms(time.time(), start_time)
    print_simple_product(position, row['Handle'], f'{execution_time} ms')

def include_index(): return ('-i' in sys.argv)

# Output results to spreadsheet 
pwd = os.getcwd()
shopify_df_csv_output.to_csv(OUTPUT_PATH, index=include_index())
print_info(f'Shopify Products Import CSV generated at: {pwd}/{OUTPUT_PATH}')
custom_options.to_xlsx()
print_info(f'Number of customized options: {custom_options_count}')


# Log script timing
script_time_in_total_secs = int(time.time() - script_start_time)
script_time_in_min = int(script_time_in_total_secs / 60)
script_time_in_remaining_secs = script_time_in_total_secs % 60
if (script_time_in_total_secs > 60):
    print_info(f'Script completed in {script_time_in_min} minutes and {script_time_in_remaining_secs} seconds')
else:
    print_info(f'Script completed in {script_time_in_total_secs} seconds')

