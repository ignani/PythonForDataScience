import pandas as pd
import numpy as np
import re

# productList = pd.read_csv('Data/flipkartProductReview.csv', index_col = 'uniq_id', usecols = ['uniq_id', 'product_name', 'pid']) #, nrows = 5)
productList = pd.read_csv('Utilities/Products_2K.csv')
# productList = pd.read_csv('Utilities/ProductList.csv')
productList.shape

# drop all rows where product_name is empty
productList.drop(productList[~productList.product_name.notnull()].index, inplace = True)

# Sort values based on product_name
productList.sort_values("product_name", axis = 0, ascending = True, inplace = True, na_position = 'first')

# dropping ALL duplicte values
data.drop_duplicates(subset ="First Name", keep = False, inplace = True)
uniqueSKUs = set(productList.product_name.str.lower())
len(uniqueSKUs)
productList.shape


re.findall(r"\W+",'Caress Velvet Bliss Ultra Silkening Beauty Bar Qty 6 Ct')

uniqueSKUs = pd.DataFrame(uniqueSKUs)

from quantulum3 import parser
item = parser.parse('Caress Velvet Bliss Ultra Silkening Beauty Bar Qty 6 Ct')
" ".join([(x.surface) for x in item])
item
x = productList.groupby(['product_name', 'generic_name', 'quantity', 'brands', 'brands_tags', 'categories', 'categories_tags', 'categories_en'])['product_name'].count()
x.shape
# sort the data in the dataframe
productList.sort_values(['product_name', 'pid'], inplace = True)

# Duplicate the product_name column

# Split the Duplicate into and convert to lowercase
# Weight into separate column
# Stopwords into separate columns
# Name


x = productList.groupby('product_name')['product_name'].count().sort_values(ascending=False)


