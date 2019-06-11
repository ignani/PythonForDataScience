"""
How to determine the optimal number of clusters for k-means clustering
----------------------------------------------------------------------

**K-means** is a type of unsupervised learning and one of the popular methods of clustering unlabelled data into k clusters.
One of the trickier tasks in clustering is identifying the appropriate number of clusters k.
In this tutorial, we will see how to use the elbow method as a way to estimate the value k.
Another popular method of estimating k is through silhouette analysis, a scikit learn example can be found @ https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html.

We will use the wholesale customer dataset which can be downloaded @ https://www.kaggle.com/binovi/wholesale-customers-data-set.

**K-means Overview:**
 Before diving into the dataset, let us briefly discuss how k-means works:
    - The process begins with k centroids initialised at random.
    - These centroids are used to assign points to its nearest cluster.
    - The mean of all points within the cluster is then used to update the position of the centroids.
    - The above steps are repeated until the values of the centroids stabilise.

**Getting Started**
 In this tutorial, we will be using the scikit-learn’s implementation of k-means which can be found here

**The dataset**
The dataset we will study refers to clients of a wholesale distributor.
It contains information such as clients annual spend on fresh product, milk products, grocery products etc. Below is some more information an each feature:
    - FRESH: annual spending (m.u.) on fresh products (Continuous)
    - MILK: annual spending (m.u.) on milk products (Continuous)
    - GROCERY: annual spending (m.u.) on grocery products (Continuous)
    - FROZEN: annual spending (m.u.) on frozen products (Continuous)
    - DETERGENTS_PAPER: annual spending (m.u.) on detergents and paper products (Continuous)
    - DELICATESSEN: annual spending (m.u.) on delicatessen products (Continuous)
    - CHANNEL: customer channels - Horeca (Hotel/Restaurant/Cafe) or Retail channel (Nominal)
    - REGION: customer regions - Lisnon, Oporto or Other (Nominal)
"""

# Import required packages
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Read in data and inspect the first 5 records.
data = pd.read_csv('Data/Wholesale customers data.csv')

# Below is a split of categorical and continuous features
categorical_features = ['Channel', 'Region']
continuous_features = ['Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen']

# Descriptive statistics below shows on average clients spend the most on fresh groceries and the least on delicassen.
data[continuous_features].describe()

# To use the categorical features, we need to convert the categorical features to binary using pandas get dummies.
for col in categorical_features:
    dummies = pd.get_dummies(data[col], prefix=col)
    data = pd.concat([data, dummies], axis=1)
    data.drop(col, axis=1, inplace=True)

# To give equal importance to all features, we need to scale the continuous features.
# We will be using scikit-learn’s MinMaxScaler as the feature matrix is a mix of binary and continuous features.
# Other alternatives includes StandardScaler.
mms = MinMaxScaler()
mms.fit(data)
data_transformed = mms.transform(data)

#For each k value, we will initialise k-means and use the inertia attribute to identify the sum of squared distances of samples to the nearest cluster centre.
Sum_of_squared_distances = []
K = range(1,15)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(data_transformed)
    Sum_of_squared_distances.append(km.inertia_)

# As k increases, the sum of squared distance tends to zero.
# Imagine we set k to its maximum value n (where n is number of samples) each sample will form its own cluster meaning sum of squared distances equals zero.

# Below is a plot of sum of squared distances for k in the range specified above. If the plot looks like an arm, then the elbow on the arm is optimal k.
plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()

# In the plot above the elbow is at k=5 (or k-6) indicating the optimal k for this dataset is 5/6 depending on what you consider as the elbow region.
# While from 5 onwards it starts to slow down, you can also see there is a lot of difference in point 6 and the rest.
# Hence, 5 or 6 can be selected as the optimal k depending on your requirements.
# The actual number of clusters chosen can be finally be based on business context and convenience of dealing with number of segments or clusters.
