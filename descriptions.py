import time
import pandas as pd

IMPORT_PATH = 'data/catalog_product_20210403_173129.csv'
raw_magento_product_csv = pd.read_csv(IMPORT_PATH, low_memory=False)

sku_is_not_nan = pd.isna(raw_magento_product_csv['sku']) == False
magento_df: pd.DataFrame = raw_magento_product_csv[sku_is_not_nan]

description_contains_link = magento_df['short_description'].str.contains(r'<a.*?>')
magento_df: pd.DataFrame = magento_df[description_contains_link]

def sanitize_input(input: str, replacement: str):
    if pd.isna(input): return ''

    sanitized = input.replace('\r\n', replacement)
    sanitized = sanitized.replace('\r', replacement)
    sanitized = sanitized.replace('\n', replacement)
    sanitized = sanitized.replace('\t', replacement)
    return sanitized

def to_body_html_column(input: str): return sanitize_input(input, '<br/>')
magento_df['short_description'] = magento_df['short_description'].apply(to_body_html_column)

magento_df = magento_df.reset_index()

df = pd.DataFrame(
    data={
        "Product Title": magento_df['name'],
        "Shopify Public URL": magento_df['url_key'], 
        "Original Description": magento_df['short_description']
    }
)

url = 'https://columbiagemhouse.myshopify.com/products/'
df['Shopify Public URL'] = url + df['Shopify Public URL'].astype(str)

NOW_DATE_TIME = time.strftime("%Y%m%d_%H%M%S")
OUTPUT_PATH = f'data/shopify_products_with_links_in_descriptions_{NOW_DATE_TIME}.csv'

df.to_csv(OUTPUT_PATH, index=False)