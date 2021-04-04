import pandas as pd
from typing import List

IMPORT_PATH = 'data/catalog_product_20210403_173129.csv'
OUTPUT_PATH = 'data/output.csv'

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
products = raw_products.drop(columns=unused_columns)

# Utilities
num_of_rows = products.shape[0]
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

published_column = list(map(to_published, products['status']))
published_column = backfill_array(published_column)

# Status column
def to_status(value: int): 
    if value == 1:
        return 'active'
    elif value == 2:
        return 'draft'
    else:
        return ''

status_column = list(map(to_status, products['status']))
status_column = backfill_array(status_column)

# Img Src column
def generate_url(ext): 
    img_base = 'https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95'
    if (type(ext) is str):
        return img_base + ext
    else:
        return ''

img_src_column = list(map(generate_url, products['_media_image']))



# Format to match Shopify import shape
output = { 
    'Handle': products['url_key'],
    'Title': products['name'],
    'Body (HTML)': products['short_description'],
    'Vendor': empty_column,
    'Type': products['_category'],
    'Tags': empty_column,
    'Published': published_column,
    'Option1 Name': empty_column, # Needs work
    'Option1 Value': empty_column, # Needs work
    'Option2 Name': empty_column, # Needs work
    'Option2 Value': empty_column, # Needs work
    'Option3 Name': empty_column, # Needs work
    'Option3 Value': empty_column, # Needs work
    'Variant SKU': empty_column,
    'Variant Grams': empty_column, # needs converstion
    'Variant Inventory Tracker': empty_column,  
    'Variant Inventory Qty': products['qty'],
    'Variant Inventory Policy': generate_column('deny'), 
    'Variant Fulfillment Service': generate_column('manual'),
    'Variant Price': products['price'], 
    'Variant Compare At Price': empty_column, 
    'Variant Requires Shipping': generate_column('TRUE'), 
    'Variant Taxable': generate_column('TRUE'), 
    'Variant Barcode': empty_column,
    'Image Src': img_src_column, 
    'Image Position': empty_column,
    'Image Alt Text': products['_media_lable'], 
    'Gift Card': generate_column('FALSE'),
    'SEO Title': products['meta_title'],
    'SEO Description': products['meta_description'],
    'Variant Weight Unit': generate_column('g'),
    'Status': status_column, 
}

output = pd.DataFrame(data=output) 

output.to_csv(OUTPUT_PATH)
