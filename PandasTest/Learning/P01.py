import pandas as pd
import numpy as np
import os

os.chdir("E:\\DataScience\\Data\\PluralPandasFundamentals\\02\\demos\\collection-master")

inputDF = pd.read_csv("artwork_data.csv", index_col="id", dtype={'dimensions': 'str'}) #, nrows=100)

artists = inputDF["artist"]  # extract the list of artists from the data frame
uniqueArtists = pd.unique(artists)  # Extract unique names of the artists
print(len(uniqueArtists))

inputDF.shape  # Count of rows, columns
inputDF.shape[0]  # count of rows
inputDF.shape[1]  # count of columns

# Filtering the Dataframe
s = inputDF["artist"] == "Blake, Robert"  # Filters all the records and returns a series mentioning if the condition is true or false
s.value_counts()  # returns the number of true and false count

# Filtering with a different approach
artistsCount = inputDF["artist"].value_counts()
artistsCount["Blake, Robert"]

# Indexing and Filtering
# DataFrame.loc
inputDF.loc[1037, 'artist']  # provide the row label and the column label
inputDF.loc[inputDF['artist'] == 'Blake, Robert',:]  # here we are filtering by providing the condition and the : in the column indexer says we need all the columns

# DataFrame.iloc    - It uses the index instead of labels
inputDF.iloc[0, 0]  # get value from first row and first column
inputDF.iloc[10, :]  # get all columns from first row
inputDF.iloc[:, 0]  # get all rows from first column
inputDF.iloc[2:6, [1, 2, 3]]  # here am actually asking for rows from 2 to 6 (zero index) and columns 2,3,4


inputDF.head(n=5)
inputDF['width'].sort_values().head()
inputDF['width'].sort_values().tail()
inputDF['width'] * inputDF['height']  # multiplication, but this will not work, since the dtype is object. Convert and try.

# Convert Data types
pd.to_numeric(inputDF['height'])  # when the value cannot be converted, it will throw an error
pd.to_numeric(inputDF['height'], errors='coerce')  # when a value cannot be converted, say in case of null, it will change it to NaN. This doesn't convert the actual values
inputDF.loc[:, 'height'] = pd.to_numeric(inputDF['height'], errors='coerce')  # Here we are converting and then writing the values back to the dataframe
inputDF.loc[:, 'width'] = pd.to_numeric(inputDF['width'], errors='coerce')  # Here we are converting and then writing the values back to the dataframe

area = inputDF['height'] * inputDF['width']  # Creating a new series
inputDF = inputDF.assign(area=area)  # Adding the series as a column into the dataframe

inputDF['area'].max()  # get the max value from area column
inputDF['area'].idxmax()  # get the id of the row which contains the max value of area
inputDF.loc[inputDF['area'].idxmax(), :]  # uses the id to get the row

# GROUPING AND AGGREGATION
# ITERATION
small_df = inputDF.iloc[49000:50019, :].copy()
grouped = small_df.groupby('artist')
type(grouped)

for name, group_df in grouped:
    print(name)
    print(group_df)
    break

# Aggregate
# Mins
for name, group_df in small_df.groupby('artist'):
    min_year = group_df['acquisitionYear'].min()
    print("{}: {}".format(name, min_year))


# Transform
# Equivalent of editing by hand:
# Make a case when there is no data to infer
# small_df.loc[[11838, 16441], 'medium'] = np.nan
def fill_values(series):
    values_counted = series.value_counts()
    if values_counted.empty:
        return series
    most_frequent = values_counted.index[0]
    new_medium = series.fillna(most_frequent)
    return new_medium


def transform_df(source_df):
    group_dfs = []
    for name, group_df in source_df.groupby('artist'):
        filled_df = group_df.copy()
        filled_df.loc[:, 'medium'] = fill_values(group_df['medium'])
        group_dfs.append(filled_df)

    new_df = pd.concat(group_dfs)
    return new_df


# Now check the result
filled_df = transform_df(small_df)

# BUILT-INS
# Transform
grouped_mediums = small_df.groupby('artist')['medium']
small_df.loc[:, 'medium'] = grouped_mediums.transform(fill_values)      # insteading of writing our own transform function, we can use the built in function

# Min
inputDF.groupby('artist').agg(np.min)
inputDF.groupby('artist').min()

# Filter
grouped_titles = inputDF.groupby('title')
title_counts = grouped_titles.size().sort_values(ascending=False)

condition = lambda x: len(x.index) > 1
dup_titles_df = grouped_titles.filter(condition)
dup_titles_df.sort_values('title', inplace=True)
