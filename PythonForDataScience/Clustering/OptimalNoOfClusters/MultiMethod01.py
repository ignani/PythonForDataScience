"""
Finding Optimal Number of Clusters
----------------------------------

    This tutorial explains how to find optimal number of clusters in a given dataset by using various techniques.
    Different techniques discussed here are
        Dendogram
        Elbow Method
        Silhoutte Score Analysis

    We will first load the daa into dataframe and scale the features and then create clusters.
    And then various metrics are calculated to validate the number of cluster creations and what will be the optimal number of clusters.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

beers = pd.read_csv("Data/beers.csv")

'''
Attribute Description
    name - the beer brand
    calories - calories per ounce
    sodium
    alcohol - percentage present
    cost - in dollars
'''