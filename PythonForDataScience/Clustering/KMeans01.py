"""
Using K-Means Clustering when there is Mixed Data
-------------------------------------------------
For clustering using KMeans, your data must be real continuous number, though integers can be used, it doesn't work well. And when it comes to binary data, it works, but not advisable to use and the results will not be correct.

Moreover, since KMeans is using euclidean distance, having categorical column is not a good idea. It doesn't work and the clusters will not have any meaning. Therefore you should also encode the categorical data (using One Hot Encoding, Binary, or any suitable encoding methods depending on the type of the data) In this example, the column timeOfDay is encoded using One Hot Encoding into three dummy variables.

Lastly, the data as to be standardized. It may not be important in the case of the sample we have taken, but in general, you risk that the algorithm will be pulled into direction with largest values, which is not what you want.


If you have variables with unique values (e.g, Id, TimeStamp, Transaction Number, etc), just keep them out, it will only confuse the algorithm.

Sample Data:

       Wattage        time_stamp       timeOfDay   Duration (s)
    0    100      2015-02-24 10:00:00    Morning      30
    1    120      2015-02-24 11:00:00    Morning      27
    2    104      2015-02-24 12:00:00    Morning      25
    3    105      2015-02-24 13:00:00  Afternoon      15
    4    109      2015-02-24 14:00:00  Afternoon      35
    5    120      2015-02-24 15:00:00  Afternoon      49
    6    450      2015-02-24 16:00:00  Afternoon      120
    7    200      2015-02-24 17:00:00    Evening      145
    8    300      2015-02-24 18:00:00    Evening      65
    9    190      2015-02-24 19:00:00    Evening      35
    10   100      2015-02-24 20:00:00    Evening      45
    11   110      2015-02-24 21:00:00    Evening      100
"""

import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('C:/.../Dataset.csv',sep=';')

#Make a copy of DF
df_tr = df

#Transsform the timeOfDay to dummies
df_tr = pd.get_dummies(df_tr, columns=['timeOfDay'])

#Standardize
clmns = ['Wattage', 'Duration','timeOfDay_Afternoon', 'timeOfDay_Evening', 'timeOfDay_Morning']
df_tr_std = stats.zscore(df_tr[clmns])

#Cluster the data
kmeans = KMeans(n_clusters=2, random_state=0).fit(df_tr_std)
labels = kmeans.labels_

#Glue back to originaal data
df_tr['clusters'] = labels

#Add the column into our list
clmns.extend(['clusters'])

#Lets analyze the clusters
print(df_tr[clmns].groupby(['clusters']).mean())

#Scatter plot of Wattage and Duration
sns.lmplot('Wattage', 'Duration',
           data=df_tr,
           fit_reg=False,
           hue="clusters",
           scatter_kws={"marker": "D", "s": 100})
plt.title('Clusters Wattage vs Duration')
plt.xlabel('Wattage')
plt.ylabel('Duration')