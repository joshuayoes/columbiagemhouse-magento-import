# Columbia Gem House Magento To Shopify Import

## Getting Started (Linux/Unix/MacOS enviroment)

1. Install git repository locally.
2. Run `python3 -m pip install -r requirements.txt` to install dependencies.
3. Run `python3 ./products.py` in your working directory for primary script
   1. `./products.py` is the primary script for generating Shopify products, others are support modules or utility scripts.

## Files

| File/Folder  | Description |
| -----------  | ----------- |
| /data        | Folder for generated .csv files. All are ignored excent for Magento export CSVs that we use as a source |
| customers.py | Generate script for Shopify customer import from Magento |
| customoptions.py | Utility class package for generating [Infinite Product Options](https://apps.shopify.com/product-options-by-hulkapps-1) Shopify App CSV Import |
| customprices.py | Utility class package for generating [Wholesale Club](https://apps.shopify.com/product-options-by-hulkapps-1) Shopify App CSV Import |
| descriptions.py | Utility script for finding products descriptions with links in them, to trace which products would have broken links from Magento
| images.py | Utility data structure for ignoring broken Magento product image links in products.py
| products.py | **Main entrypoint**. Script for transforming Magento Product Export into [CSV import format as defined by Shopify](https://help.shopify.com/en/manual/products/import-export/using-csv#product-csv-file-format) |


## Shopify Resources

- [Shopify CSV import help article](https://help.shopify.com/en/manual/products/import-export/using-csv#get-a-sample-csv-file)
- [Shopify CSV import example](https://github.com/shopifypartners/product-csvs/blob/master/home-and-garden.csv#L3)
- [Multiple Variants example](https://community.shopify.com/c/Shopify-Discussion/Correct-format-for-importing-products-with-variants/td-p/286027)
