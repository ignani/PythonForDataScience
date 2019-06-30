"""
https://medium.com/ibm-data-science-experience/missing-data-conundrum-exploration-and-imputation-techniques-9f40abe0fd87

Exploring Data Missingness
Here, I used the datasets in the ongoing Zillow’s Home Value Prediction Competition ($1.2million prize) on Kaggle and I used a python package called missingno. This package is a very flexible missing data visualization tool built with matplotlib and it takes any pandas DataFrame thrown at it. The Kaggle/Zillow data has a training set and a properties dataset that describes the properties of all the homes. I merged both dataset and presented a plot of the missing value matrix.

"""
import numpy as np
import pandas as pd
import matplotlib
import missingno as msno
# %matplotlib inline
train_df = pd.read_csv('train_2016_v2.csv', parse_dates=["transactiondate"])
properties_df = pd.read_csv('properties_2016.csv')
merged_df = pd.merge(train_df,properties_df)
missingdata_df = merged_df.columns[merged_df.isnull().any()].tolist()
msno.matrix(merged_df[missingdata_df])

x = np.genfromtxt('E:/DataScience/PythonForDataScience/PythonForDataScience/Data/adult-train-raw.csv', delimiter = ', ', dtype = object)
df = pd.DataFrame(x)
df.info()