"""
Generic Data Importer
---------------------

Features that needs to be in this library:

- Should be able to import any csv file, irrespective of the number of columns or their names or their data types.
- The following shold be allowed through configuration:
    - Should allow column renaming
    - Should allow data formatting for individual columns.
    - Should allow for splitting and extacting data from individual columns and create a new column out of the extracted data.
    - Should allow creating hierarchies and save them to multiple files.
    - should allow exporting only necessary columns and rows.

Steps:
------
- Read the mapping column names from config file, which will include:
    - Output File Name
    - List of Output Columns. For each column, the following details will be provided.
        - Output Column name.
        - Input Column name.
        - F / P : Full or partial mapping. In case of Full mapping, it would be just renaming a column.
        - Regex : If its partial mapping, then the Regex code to split the data.
        - Data Type : To be used for validating the data.
    - List of columns to be removed from the Input File.

 Procedure:
 ----------
    - Pandas and dataframe will be used.
    - Import the csv data into pandas data frame.
    - Read the config file.
    - Remove the list of columns that are not requried.
    - Loop through each column definition and perform the operation to extract or rename.
"""

import pandas as pd
import os

#region ------ Import CSV data into dataframe
# os.chdir("E:\\DataScience\\PythonForDataScience\\PandasTest\\Data")
inputDF = pd.read_csv("PythonForDataScience/Data/titanic.csv", dtype = {'dimensions': 'str'}, low_memory = False, nrows=10)
#endregion

#region ------ Read the config file
# Import the config data into json object
import json
with open('PythonForDataScience/Data/json_sample03.json') as jsonFile:
    importConfig = json.load(jsonFile)
#endregion

#region ------ Delete unwanted columns
# we need to do this here, so that the size of the dataframe would be small, to increase performance
inputDF.drop(importConfig["ToDelete"], axis = 1, inplace = True)

#endregion

for column in importConfig["OColumns"]:
    print(column)

x = inputDF.drop(importConfig["ToDelete"], axis = 1)

if importConfig["OColumns"][0]["Mapping"] == 'F':
    x.rename(columns={importConfig["OColumns"][0]["IName"]:importConfig["OColumns"][0]["OName"]},inplace = True)
#else:
    # x[importConfig["OColumns"][0]["OName"]] = inputDF['name'].str.extract()