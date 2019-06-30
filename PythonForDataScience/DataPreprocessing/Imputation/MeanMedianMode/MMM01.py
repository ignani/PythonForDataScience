"""
https://scikit-learn.org/stable/modules/impute.html

Datasets contain missing values, often encoded as blanks, NaNs or other placeholders.
Such datasets however are incompatible with scikit-learn estimators which assume that all values in an array are numerical,
and that all have and hold meaning.

Scikit learn library provides option to impute values various algorithms.
- Univariate imputation
    which imputes values in the i-th feature dimension using only non-missing values in that feature dimension (e.g. impute.SimpleImputer).
- Multivariate imputation
    use the entire set of available feature dimensions to estimate the missing values (e.g. impute.IterativeImputer).

This sample covers imputing the missing values using Univariate imputation

The SimpleImputer class provides basic strategies for imputing missing values.
Missing values can be imputed with a provided constant value, or using the statistics (mean, median or most frequent) of each column in which the missing values are located. This class also allows for different missing values encodings.

"""
import numpy as np
from sklearn.impute import SimpleImputer

# The following snippet demonstrates how to replace missing values, encoded as np.nan, using the mean value of the columns (axis 0) that contain the missing values:
imp = SimpleImputer(missing_values=np.nan, strategy='mean')
imp.fit([[1, 2], [np.nan, 3], [7, 6]])
SimpleImputer(add_indicator=False, copy=True, fill_value=None, missing_values=nan, strategy='mean', verbose=0)
X = [[np.nan, 2], [6, np.nan], [7, 6]]
imp.transform(X)

# [[4.          2.        ]
#  [6.          3.666...]
#  [7.          6.        ]]
# The SimpleImputer class also supports sparse matrices:
#
# >>>
# >>> import scipy.sparse as sp
# >>> X = sp.csc_matrix([[1, 2], [0, -1], [8, 4]])
# >>> imp = SimpleImputer(missing_values=-1, strategy='mean')
# >>> imp.fit(X)
# SimpleImputer(add_indicator=False, copy=True, fill_value=None,
#               missing_values=-1, strategy='mean', verbose=0)
# >>> X_test = sp.csc_matrix([[-1, 2], [6, -1], [7, 6]])
# >>> print(imp.transform(X_test).toarray())
# [[3. 2.]
#  [6. 3.]
#  [7. 6.]]
# Note that this format is not meant to be used to implicitly store missing values in the matrix because it would densify it at transform time. Missing values encoded by 0 must be used with dense input.
#
# The SimpleImputer class also supports categorical data represented as string values or pandas categoricals when using the 'most_frequent' or 'constant' strategy:
#
# >>>
# >>> import pandas as pd
# >>> df = pd.DataFrame([["a", "x"],
# ...                    [np.nan, "y"],
# ...                    ["a", np.nan],
# ...                    ["b", "y"]], dtype="category")
# ...
# >>> imp = SimpleImputer(strategy="most_frequent")
# >>> print(imp.fit_transform(df))
# [['a' 'x']
#  ['a' 'y']
#  ['a' 'y']
#  ['b' 'y']]