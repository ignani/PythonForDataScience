import pandas as pd
import numpy as np

# df = pd.read_csv('en.openfoodfacts.org.products.csv', error_bad_lines=False, sep = '\t', usecols = ['product_name','generic_name', 'quantity', 'brands', 'brands_tags', 'categories', 'categories_tags', 'categories_en'])

# groups = df.groupby(np.arange(len(df.index))/10000)
# for (frameno, frame) in groups:
#     frame.to_csv("%s.csv" % frameno,header=True,index=False,encoding="ISO-8859-1")
#
# print(df.head(2000).to_csv("test.csv",header=True,index=False,encoding="ISO-8859-1"))

df = pd.read_csv('Utilities/test_0.csv')
# for x in range(0, 1138874, 10000):
#     df.head(2000).to_csv("test_"+str(x)+".csv", header = True, index = False)

x = df.groupby('product_name','generic_name', 'quantity', 'brands', 'brands_tags', 'categories', 'categories_tags', 'categories_en')['product_name'].count().sort_values(ascending=True)