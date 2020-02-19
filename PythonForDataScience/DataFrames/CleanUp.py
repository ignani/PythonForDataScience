import pandas as pd
import numpy as np

data = {'Name': ['John', 'Paul', '', 'Wale', 'Mary', 'Carli', 'Steve'], 'Age': [21, 23, np.nan, 19, 25, np.nan, 15], 'Sex': ['M', np.nan, np.nan, 'M', 'F', 'F', 'M'],
        'Goals': [5, 10, np.nan, 19, 5, 0, 7], 'Assists': [7, 4, np.nan, 9, 7, 6, 4], 'Value': [55, 84, np.nan, 90, 63, 15, 46],
        'PoliticalAffiliation': [1, 2, 3, 2, np.NaN, 1, 3]}
df = pd.DataFrame(data, columns = ['Name', 'Age', 'Sex', 'Goals', 'Assists', 'Value'])

df.shape