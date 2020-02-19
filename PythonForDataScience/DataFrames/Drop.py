"""
CaseDeletion Methods
-------------

In order for these methods to produce appropriate results in most situations, data must be what is known as MCAR - Missing completely at Random.
In other words, it means that the missing values must be unrelated to the observed values.
Some more widely applicable approaches are provided by the SPSS sStatistics Missing Values Analysis option, including multiple imputation methods.

"""

import pandas as pd
import numpy as np

data = {'Name': ['John', 'Paul', '', 'Wale', 'Mary', 'Carli', 'Steve'], 'Age': [21, 23, np.nan, 19, 25, np.nan, 15], 'Sex': ['M', np.nan, np.nan, 'M', 'F', 'F', 'M'],
        'Goals': [5, 10, np.nan, 19, 5, 0, 7], 'Assists': [7, 4, np.nan, 9, 7, 6, 4], 'Value': [55, 84, np.nan, 90, 63, 15, 46],
        'PoliticalAffiliation': [1, 2, 3, 2, np.NaN, 1, 3]}
df = pd.DataFrame(data, columns = ['Name', 'Age', 'Sex', 'Goals', 'Assists', 'Value'])

df.shape


# -------------------------------------------------------------------------------------------------------------------
# a. Listwise / Complete Case Analysis
# -------------------------------------------------------------------------------------------------------------------
#   Listwise or Complete Case Deletion removes all the data for an observation that has one or more missing values.
#   If the missing data is limited to a small number of observations, you may just opt to delete those cases from the analysis.
#   However in most cases, it is often disadvantageous to use this method. This is because, the assumptions of MCAR are typically rare to support.
#   As a result, listwise deletion methods produce biased parameters and estimates.
#
#   Syntax:
# 	    DataFrameName.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
#   Parameters:
# 	    • axis: axis takes an int or string value for rows/columns. Input can be 0 or 1 for Integer and ‘index’ or ‘columns’ for String.
# 	    • how: how takes string value of two kinds only (‘any’ or ‘all’). ‘any’ drops the row/column if ANY value is Null and ‘all’ drops only if ALL values are null.
# 	    • thresh: thresh takes integer value which tells minimum amount of na values to drop.
# 	    • subset: It’s an array which limits the dropping process to passed rows/columns through list.
# 	    • inplace: It is a boolean which makes the changes in data frame itself if True.

# Pandas dropna() method allows the user to analyze and drop Rows/Columns with Null values in different ways.
df.dropna(inplace = True)

# Example 01: Dropping rows with atleast one null value. It returns a new dataframe with the results.
newDF = df.dropna(axis = 0, how = 'any')

# Example 02: Changing axis and using 'how' and 'inplace' parameters.
# Drops columns with all null values only.
df.dropna(axis = 1, how = 'all', inplace = True)  # instead of number as value for axis, you can specify 'columns', which does the same.

# Example 03: Using the threshold value.
# Keep only the rows with atleast 2 non NA values.
df.dropna(thresh = 2)

# -------------------------------------------------------------------------------------------------------------------
# b. Pairwise
# -------------------------------------------------------------------------------------------------------------------
#   Pairwise deletion analyses all cases in which the variables of interest are present and thus maximizes all data available by an analysis basis.
#   A strength to this technique is that it increases power in your analysis but it has many disadvantages. It assumes that the missing data are MCAR.
#   If you delete pairwise then you’ll end up with different numbers of observations contributing to different parts of your model, which can make interpretation difficult.

# Example 01: Using the columns that are needed for analysis.
# Define the list of columns to look for missing values. Here we are using two columns for analysis, which we specify as parameter.
#
# Pairwise deletion is an alternative to listwise deletion to mitigate the loss of data.
# Hence for your analysis in this example, all cases with available data on Age and Political affiliation will be included regardless of the missing values for other variables like gender, income or education.

df.dropna(subset = ['Age', 'PoliticalAffiliation'], inplace = True)

# -------------------------------------------------------------------------------------------------------------------
# c. Dropping Variables
# -------------------------------------------------------------------------------------------------------------------
#   It is always better to keep data than to discard it. Sometimes you can drop variables if the data is missing for more than 60% observations but only if that variable is insignificant.
# Having said that, imputation is always a preferred choice over dropping variables


del df['Name'] # Delete the name variables
df.drop('Age', axis = 1, inplace = True)    # Same as above. We are dropping or deleting the Age variable in this case.

# -------------------------------------------------------------------------------------------------------------------
# c. Dropping Variables based on condition
# -------------------------------------------------------------------------------------------------------------------
df.drop(df[df['Age'] < 20].index, inplace = True)

# drop rows where a column has null values
df.drop(df[~df.Age.notnull()].index, inplace = True)