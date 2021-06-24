import os
from typing import Tuple
import pandas as pd
import time
import pycountry
import re
import phonenumbers

NOW_DATE_TIME = time.strftime("%Y%m%d_%H%M%S")
IMPORT_PATH = 'data/customer_20210624_214051.csv'
OUTPUT_PATH = f'data/shopify_customer_import_{NOW_DATE_TIME}.csv'

headers = ['email','_website','_store','confirmation','created_at','created_in','customer_account_number','disable_auto_group_change','dob','firstname','gender','group_id','lastname','mgs_social_fid','mgs_social_ftoken','mgs_social_gid','mgs_social_gtoken','mgs_social_tid','mgs_social_ttoken','middlename','password_created_at','password_hash','prefix','rp_customer_id','rp_token','rp_token_created_at','store_id','suffix','taxvat','website_id','password','_address_city','_address_company','_address_country_id','_address_fax','_address_firstname','_address_lastname','_address_postcode','_address_prefix','_address_region','_address_street','_address_suffix','_address_telephone','_address_vat_id','_address_default_billing_','_address_default_shipping_']
dtypes = {}
for column in headers:
    dtypes[column] = 'str'

raw_magento_customer_csv = pd.read_csv(IMPORT_PATH, low_memory=False, dtype=dtypes)
 
# Filter out additional rows to add non-default address
magento_customer: pd.DataFrame = raw_magento_customer_csv[raw_magento_customer_csv['email'].notnull()]

num_of_rows = magento_customer.shape[0]
def generate_column(input): return [input] * num_of_rows
empty_column = generate_column('')

full_address: Tuple[pd.Series, pd.Series] = magento_customer['_address_street'].str.split('\n', 1, expand=True)
address1 = full_address[0]
address2 = full_address[1]

def to_address1(address: str):
    if pd.isna(address): return "" 
    
    if address == 'Ko-po ishii303':
        return '4-30-13 Higashiikebukuro'

    if address == '199 ladkrabang industrial estate. EPZ3/2, Chalongkrung Rd, Lamplatiew':
        return '199 E3/2 EPZ 3 LATKRABANG INDUSTRIAL ESTATE. CHALONGKRUNG ROAD'
    
    return address
    
def to_address2(address: str):
    if pd.isna(address): return "" 
    
    if address == ', 4-30-13, Higashiikebukuro':
        return 'Ko-po ishii303'
    
    return address

address1 = list(map(to_address1, address1))
address2 = list(map(to_address2, address2))



def to_province_code(row: pd.Series):
    province, city, street = row._values
    
    if pd.isna(city):
        return ""

    if province == 'Montana': return "MT"
    if province == 'Maryland': return 'MD'

    try:
        item = pycountry.subdivisions.lookup(province)
        code = re.sub(r'\w{2}-', '', item.code)
    except LookupError:
        code = ''
        if province == 'Brisbane': code = 'WA' 
        if province == 'South Yorkshire': code = 'BNS'
        if province == 'GJ': code = 'GJ'
        if province == 'NSW': code = 'NSW'
        if province == 'NSW ': code = 'NSW'
        if province == 'Chieti - Abruzzo -': code = 'CH'
        if province == 'Neuenburg': code = 'NE'
        if province == 'VIC': code = 'VIC'
        if province == 'Genf': code = 'GE'
        if province == 'WA': code = 'WA'
        if province == 'Herefordshire ': code = 'HEF'
        if province == 'Falmouth,Cornwall': code = 'CON'
        if province == 'Yucatan': code = 'YUC'
        if province == 'Bangkok': code = '10'
        if province == 'Gyeonggi-do': code = '41'
        if province == 'Daejeon': code = '30'
        if province == 'Skåne': code = 'M'
        if province == 'Singapore': code = '01'
        if province == 'Gloucestershire ': code = 'GLS'
        if province == 'London': code = 'KEC'
        if province == 'Al Asimah': code = 'KU'
        if province == 'Derbyshire ': code = 'DBY'
        if province == 'Cheshire': code = 'CHE'
        if province == 'Maryland': code = 'MD'
        if city == 'Nelson': code = 'NSN'
        if street == '17 Grove Mansions': code = 'WND'
        if city == 'hochiminh': code = 'SG'
        if city == 'Eskilstuna': code = 'D'
        if city == 'Newcastle Upon Tyne': code = 'NET'
        if city == 'Beijing': code = 'BJ'
        if city == 'Copenhagen K': code = '84'
        if city == 'Copenhagen ': code = '84'
        if city == 'Rotterdam': code = 'ZH'
        if city == 'Staines': code = 'SRY'
        if city == 'Eidsfoss': code = '38'
        if city == 'Singapore': code = '01'
        if city == 'Herent': code = 'VLG'
        if city == 'Utrecht': code = 'UT'
        if city == 'Auckland': code = 'AUK'
        if city == 'Santo Domingo': code = '01'
        if city == 'GOTHENBORG': code = 'O'
        if city == 'Kopavogur': code = '1'
        if city == 'dundee': code = 'DND'
        if city == 'Baku': code = 'BA'
        if city == 'Nedlands': code = 'WA'
        if city == 'Tsim Sha Tsui': code = 'HK'
        if city == 'Perth': code = 'WA'
        if street == '41B Marylands Road': code = 'WSM'
        if city == 'ERSKINEVILLE': code = 'NSW'
        if city == 'Dartmouth ': code = 'NS'
        if city == 'Vasterhaninge': code = 'D'
        if city == ' Kusterdingen - Wankheim': code = 'BW'
        if city == 'Hamilton': code = 'BM'
        if city == 'Hereford': code = 'HEF'
        if street == '61b jamestown road': code = 'CMD'
        if street == 'Flat 5, 264 Waterloo Road': code = 'SWK'
        if street == 'Studio 211 Cockpit Arts\n18-22 Creekside': code = 'LEW'
        if city == 'kaohsiung': code = 'KHH'
        if city == 'Stockholm': code = 'AB'
        if city == 'Bristol': code = 'BST'
        if city == 'Tokyo  \n': code = '13'
        if city == 'Toyko ': code = '13'
        if street == '1-20-11 Shibuya \nShibuyaku': code = '13'
        if city == 'Glasgow': code = 'GLG'
        if street == '26 Poynders Court\nPoynders Road': code = 'LBH'
        if city == 'Barcelona': code = 'CT'
        if city == 'Brescia': code = 'BS'
        if city == 'Kuala Lumpur': code = '14'
        if street == '7 Bleeding Heart Yard\nHatton Garden': code = 'ISL'
        if city == 'Hong long ': code = 'HK'
        if city == 'Hong Kong': code = 'HK'
        if street == "Unit 3.02, The Goldsmiths' Centre\n42 Britton Street": code = 'ISL'
        if street == '1 Eskmont Ridge': code = 'ISL'
        if city == 'Queenstown': code = 'OTA'
        if street == 'Studio 10, 7 Tiltman Place, London, N7 7EL': code = 'ISL'
        if city == 'Izegem': code = 'VLG'
        if city == 'Amsterdam': code = 'NH'
        if city == 'Vanves': code = 'IDF'
        if city == 'Quito': code = 'P'
        if street == '40 Gladsmuir Road\n40 Gladsmuir Road': code = 'ISL'
        if city == 'Dubai': code = 'DU'
        if city == 'Lower Hutt': code = 'WGN'
        if street == '53 King George Street': code = 'GRE'
        if street == '42 Gortin Road\nKilrea': code = 'LDY'

    return code

province_code: pd.DataFrame = magento_customer[['_address_region', '_address_city', '_address_street']].apply(to_province_code, axis=1)



def to_province(isocode: str):
    if pd.isna(isocode): return "" 

    if isocode == 'US-MY': isocode = 'US-MD'
    if isocode == 'NO-38': return 'Vestfold og Telemark'
    if isocode == 'HK-HK': isocode = 'CN-HK'
    if isocode == 'BM-BM': return 'Bermuda'
    if isocode == 'GB-LDY': isocode = 'IE-U'
    if isocode == 'ES-CT': 
        return 'Catalonia Province'
    if isocode == 'JP-13': return 'Tokyo'
    if isocode == 'TH-10': return 'Bangkok'
    if isocode == 'KR-41': return 'Gyeonggi'
    if isocode == 'KR-30': return 'Daejeon'

    try:
        item = pycountry.subdivisions.lookup(isocode)
        name = item.name
    except LookupError:
        name = ""

    return name

province: pd.DataFrame = magento_customer['_address_country_id'] + '-' + province_code
province = list(map(to_province, province))



def to_country_name(code: str):
    if pd.isna(code):
        return ""

    if code == 'KR': 
        return 'South Korea'
    
    try:
        item = pycountry.countries.get(alpha_2=code)
        name = item.name
    except:
        name = ''

    return name

country = list(map(to_country_name, magento_customer['_address_country_id']))



def to_city(city: str):
    if pd.isna(city):
        return ""

    if city == 'Toshima-ku': return 'Toshima City'
    if city == 'Tokyo': return 'Shibuya City'
    if city == 'toyamacity': return 'Toyama'

    return city

city = list(map(to_city, magento_customer['_address_city']))



def to_zip(zip: str):
    if pd.isna(zip): return ""

    if zip == "Spain": "08003"

    return zip

zip = list(map(to_zip, magento_customer['_address_postcode']))



customer_group = ['NOT LOGGED IN', 'General', 'Wholesale', 'Retailer', 'anonymous user', 'authenticated user', 'product admin', 'Purchase on Account', 'anonymous user', 'Special Customer Group']
def to_tags(id: str):
    if pd.isna(id):
        return ""
    
    id = int(id)

    return customer_group[id]

tags = list(map(to_tags, magento_customer['group_id']))

def format_phone(row: pd.Series):
    input, _region = row._values

    if pd.isna(input):
        return ""

    if pd.isna(_region):
        _region = None

    try: 
        phonenumbers.parse(input, region=_region)
    except phonenumbers.phonenumberutil.NumberParseException:
        return ""

    phone = phonenumbers.parse(input, region=_region)

    if phonenumbers.is_valid_number(phone) == False:
        return ""
    
    return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

phone = magento_customer[['_address_telephone', '_address_country_id']].apply(format_phone, axis=1)


def to_note(number: str):
    if pd.isna(number):
        return ""
    
    return f'Customer Account Number: {number}'

note = magento_customer['customer_account_number'].apply(to_note)

def to_tax_exempt(row: pd.Series):
    tags, province_code = row._values

    is_wholesale = bool(re.search('Wholesale', tags, re.IGNORECASE))
    if is_wholesale == False and province_code == 'WA':
        return "no"

    return 'yes'

tax_exempt = pd.DataFrame(data={
    'tags': tags,
    'province_code': province_code
}).apply(to_tax_exempt, axis=1)

shopify_df = {
    'First Name': magento_customer['firstname'],
    'Last Name': magento_customer['lastname'],
    'Email': magento_customer['email'],
    'Company': magento_customer['_address_company'].fillna(''),
    'Address1': address1,
    'Address2': address2,
    'City': city,
    'Province': province,
    'Province Code': province_code,
    'Country': country,
    'Country Code': magento_customer['_address_country_id'].fillna(''),
    'Zip': zip,
    'Phone': phone,
    'Accepts Marketing': generate_column('yes'),
    'Total Spent': generate_column(''),
    'Total Orders': generate_column(''),
    'Tags': tags,
    'Note': note,
    'Tax Exempt': tax_exempt,
}
 
shopify_df = pd.DataFrame(data=shopify_df) 
shopify_df = shopify_df.reset_index(drop=True)

print(shopify_df[:10])

print(len(shopify_df['Email'].unique()))

pwd = os.getcwd()
print(f'Customer CSV generated at: {pwd}/{OUTPUT_PATH}')
shopify_df.to_csv(OUTPUT_PATH, index=True)
