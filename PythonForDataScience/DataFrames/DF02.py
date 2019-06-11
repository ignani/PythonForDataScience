import pandas as pd
import os

os.chdir("E:\\DataScience\\Python\\PandasTest\\Data")
data = pd.read_csv("titanic.csv")

data.head()
# data.drop(data.columns[[3]], axis=1, inplace=True)
data.iloc[0]
data.iloc[0:8]
data.loc[:, ['Name']]
data.loc[:, ['Name', 'Age']]
data.loc[data['Name'] == "Mr. Patrick Dooley"]
print(data.groupby(['Sex', 'Survived'])['Name'].count())
data.groupby(['Pclass', 'Sex'])['Age'].mean()
