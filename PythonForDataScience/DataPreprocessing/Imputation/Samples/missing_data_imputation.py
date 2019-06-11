"""
https://github.com/rafaelvalle/MDI/blob/master/missing_data_imputation.py
"""
import numpy as np
# import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from scipy.stats import mode
from scipy.linalg import svd
from collections import defaultdict


class Imputer(object):
    def __init__(self):
        """
        Attributes
        ----------

        """

    def drop(self, x, missing_data_cond):
        """ Drops all observations that have missing data

        Parameters
        ----------
        x : np.ndarray
            Matrix with categorical data, where rows are observations and
            columns are features
        missing_data_cond : function
            Method that takes one value and returns True if it represents
            missing data or false otherwise.
        """

        # drop observations with missing values
        return x[np.sum(missing_data_cond(x), axis=1) == 0]

    def replace(self, x, missing_data_cond, in_place=False):
        """ Replace missing data with a random observation with data

        Parameters
        ----------
        x : np.ndarray
            Matrix with categorical data, where rows are observations and
            columns are features
        missing_data_cond : function
            Method that takes one value and returns True if it represents
            missing data or false otherwise.
        """
        if in_place:
            data = x
        else:
            data = np.copy(x)

        for col in range(x.shape[1]):
            nan_ids = missing_data_cond(x[:, col])
            val_ids = np.random.choice(np.where(~nan_ids)[0],  np.sum(nan_ids))
            data[nan_ids, col] = data[val_ids, col]
        return data

    def summarize(self, x, summary_func, missing_data_cond, in_place=False):
        """ Substitutes missing values with a statistical summary of each
        feature vector

        Parameters
        ----------
        x : numpy.array
            Assumes that each feature column is of single type. Converts
            digit string features to float.
        summary_func : function
            Summarization function to be used for imputation
            (mean, median, mode, max, min...)
        missing_data_cond : function
            Method that takes one value and returns True if it represents
            missing data or false otherwise.
        """

        if in_place:
            data = x
        else:
            data = np.copy(x)

        # replace missing values with the summarization function
        for col in range(x.shape[1]):
            nan_ids = missing_data_cond(x[:, col])
            if True in nan_ids:
                val = summary_func(x[~nan_ids, col])
                data[nan_ids, col] = val

        return data

    def one_hot(self, x, missing_data_cond, weighted=False, in_place=False):
        """Create a one-hot row for each observation

        Parameters
        ----------
        x : np.ndarray
            Matrix with categorical data, where rows are observations and
            columns are features
        missing_data_cond : function
            Method that takes one value and returns True if it represents
            missing data or false otherwise.
        weighted : bool
            Replaces one-hot by n_classes-hot.

        Returns
        -------
        data : np.ndarray
            Matrix with categorical data replaced with one-hot rows
        """

        if in_place:
            data = x
        else:
            data = np.copy(x)

        # find rows and columns with missing data
        _, miss_cols = np.where(missing_data_cond(data))
        miss_cols_uniq = np.unique(miss_cols)

        for miss_col in miss_cols_uniq:
            uniq_vals, indices = np.unique(data[:, miss_col],
                                           return_inverse=True)
            if weighted:
                data = np.column_stack((data, np.eye(uniq_vals.shape[0],
                                        dtype=int)[indices]*uniq_vals.shape[0]))
            else:
                data = np.column_stack((data, np.eye(uniq_vals.shape[0],
                                                     dtype=int)[indices]))

        # remove categorical columns with missing data
        data = np.delete(data, miss_cols, 1)
        return data

    def knn(self, x, k, summary_func, missing_data_cond, cat_cols,
            weighted=False, in_place=False):
        """ Replace missing values with the summary function of K-Nearest
        Neighbors

        Parameters
        ----------
        x : np.ndarray
            Matrix with categorical data, where rows are observations and
            columns are features
        k : int
            Number of nearest neighbors to be used
        summary_func : function
            Summarization function to be used for imputation
            (mean, median, mode, max, min...)
        missing_data_cond : function
            Method that takes one value and returns True if it represents
            missing data or false otherwise.
        cat_cols : int tuple
            Index of columns that are categorical
        """
        if in_place:
            data = x
        else:
            data = np.copy(x)

        imp = Imputer()

        # first transform features with categorical missing data into one hot
        data_complete = imp.one_hot(data, missing_data_cond, weighted=weighted)

        # binarize complete categorical variables and convert to int
        col = 0
        cat_ids_comp = []
        while col < max(cat_cols):
            if isinstance(data_complete[0, col], np.basestring) and not data_complete[0, col].isdigit():
                cat_ids_comp.append(col)
            col += 1

        data_complete = imp.binarize_data(data_complete,
                                          cat_ids_comp).astype(float)

        # normalize features
        scaler = StandardScaler().fit(data_complete)
        data_complete = scaler.transform(data_complete)
        # create dict with missing rows and respective columns
        missing = defaultdict(list)
        map(lambda(a, b): missing[a].append(b),
            np.argwhere(missing_data_cond(data)))
        # create mask to build NearestNeighbors with complete observations only
        mask = np.ones(len(data_complete), bool)
        mask[missing.keys()] = False
        # fit nearest neighbors and get knn ids of missing observations
        print('Computing k-nearest neighbors')
        nbrs = NearestNeighbors(n_neighbors=k, metric='euclidean').fit(
            data_complete[mask])
        ids = nbrs.kneighbors(data_complete[missing.keys()],
                              return_distance=False)

        def substituteValues(i):
            row = missing.keys()[i]
            cols = missing[row]
            data[row, cols] = mode(data[mask][ids[i]][:, cols])[0].flatten()

        print('Substituting missing values')
        map(substituteValues, range(len(missing)))
        return data

    def predict(self, x, cat_cols, missing_data_cond, clf, inc_miss=True,
                in_place=False):
        """ Uses random forest for predicting missing values

        Parameters
        ----------
        cat_cols : int tuple
            Index of columns that are categorical
        missing_data_cond : function
            Method that takes one value and returns True if it represents
            missing data or false otherwise.
        clf : object
            Object with fit and predict methods, e.g. sklearn's Decision Tree
        inc_miss : bool
            Include missing data in fitting the model?
        """

        if in_place:
            data = x
        else:
            data = np.copy(x)

        # find rows and columns with missing data
        miss_rows, miss_cols = np.where(missing_data_cond(data))
        miss_cols_uniq = np.unique(miss_cols)

        if inc_miss:
            valid_cols = np.arange(data.shape[1])
        else:
            valid_cols = [n for n in range(data.shape[1])
                          if n not in miss_cols_uniq]

        # factorize valid cols
        data_factorized = np.copy(data)

        # factorize categorical variables and store transformation
        factor_labels = {}
        for cat_col in cat_cols:
            # factors, labels = pd.factorize(data[:, cat_col])
            labels, factors = np.unique(data[:, cat_col], return_inverse=True)
            factor_labels[cat_col] = labels
            data_factorized[:, cat_col] = factors

        # values are integers, convert accordingly
        data_factorized = data_factorized.astype(int)

        # update each column with missing features
        for miss_col in miss_cols_uniq:
            # extract valid observations given current column missing data
            valid_obs = [n for n in range(len(data))
                         if data[n, miss_col] != '?']

            # prepare independent and dependent variables, valid obs only
            data_train = data_factorized[:, valid_cols][valid_obs]
            y_train = data_factorized[valid_obs, miss_col]

            # train random forest classifier
            clf.fit(data_train, y_train)

            # given current feature, find obs with missing vals
            miss_obs_iddata = miss_rows[miss_cols == miss_col]

            # predict missing values
            y_hat = clf.predict(data_factorized[:, valid_cols][miss_obs_iddata])

            # replace missing data with prediction
            data_factorized[miss_obs_iddata, miss_col] = y_hat

        # replace values on original data
        for col in factor_labels.keys():
            data[:, col] = factor_labels[col][data_factorized[:, col]]

        return data

    def factor_analysis(self, x, cat_cols, missing_data_cond, threshold=0.9,
                        technique='SVD', in_place=False):
        """ Performs low-rank matrix approximation via dimensioality reduction
        and replaces missing data with values obtained from the data projected
        onto N principal components or singular values or eigenvalues...

        cat_cols : int tuple
            Index of columns that are categorical
        missing_data_cond : function
            Method that takes one value and returns True if it represents
            missing data or false otherwise.
        threshold : float
            Variance threshold that must be explained by eigen values.
        technique : str
            Technique used for low-rank approximation. 'SVD' is supported
        """

        def _mode(d):
            return mode(d)[0].flatten()

        if in_place:
            data = x
        else:
            data = np.copy(x)

        data_summarized = self.summarize(x, _mode, missing_data_cond)

        # factorize categorical variables and store encoding
        factor_labels = {}
        for cat_col in cat_cols:
            labels, factors = np.unique(data_summarized[:, cat_col],
                                        return_inverse=True)
            factor_labels[cat_col] = labels
            data_summarized[:, cat_col] = factors

        data_summarized = data_summarized.astype(float)
        if technique == 'SVD':
            lsvec, sval, rsvec = svd(data_summarized)
            # find number of singular values that explain 90% of variance
            n_singv = 1
            while np.sum(sval[:n_singv]) / np.sum(sval) < threshold:
                n_singv += 1

            # compute low rank approximation
            data_summarized = np.dot(
                lsvec[:, :n_singv],
                np.dot(np.diag(sval[:n_singv]), rsvec[:n_singv, ]))
        else:
            raise Exception("Technique {} is not supported".format(technique))

        # get missing data indices
        nans = np.argwhere(missing_data_cond(x))

        # update data given projection
        for col in np.unique(nans[:, 1]):
            obs_ids = nans[nans[:, 1] == col, 0]
            # clip low rank approximation to be within factor labels
            proj_cats = np.clip(
                data_summarized[obs_ids, col], 0, len(factor_labels[col])-1)
            # round categorical variable factors to int
            proj_cats = proj_cats.round().astype(int)
            data[obs_ids, col] = factor_labels[col][proj_cats]

        return data

    def factorize_data(self, x, cols, in_place=False):
        """Replace column in cols with factors of cols

        Parameters
        ----------
        x : np.ndarray
            Matrix with categorical data
        cols: tuple <int>
            Index of columns with categorical data

        Returns
        -------
        d : np.ndarray
            Matrix with categorical data replaced with factors
        """

        if in_place:
            data = x
        else:
            data = np.copy(x)

        factors_labels = {}
        for col in cols:
            # factors, labels = pd.factorize(data[:, col])
            labels, factors = np.unique(data[:, col], return_inverse=True)
            factors_labels[col] = labels
            data[:, col] = factors

        return data, factors_labels

    def binarize_data(self, x, cols, miss_data_symbol=False,
                      one_minus_one=True, in_place=False):
        """Replace column in cols with one-hot representation of cols

        Parameters
        ----------
        x : np.ndarray
            Matrix with categorical data, where rows are observations and
            columns are features
        cols: tuple <int>
            Index of columns with categorical data

        Returns
        -------
        d : np.ndarray
            Matrix with categorical data replaced with one-hot rows
        """

        if in_place:
            data = x
        else:
            data = np.copy(x)
        for col in cols:
            uniq_vals, indices = np.unique(data[:, col], return_inverse=True)

            if one_minus_one:
                data = np.column_stack(
                    (data,
                     (np.eye(uniq_vals.shape[0], dtype=int)[indices] * 2) - 1))
            else:
                data = np.column_stack((data, np.eye(uniq_vals.shape[0],
                                                     dtype=int)[indices]))
            # add missing data column to feature
            if miss_data_symbol is not False and \
                    miss_data_symbol not in uniq_vals:
                data = np.column_stack(
                    (data, -one_minus_one * np.ones((len(data), 1), dtype=int)))

        # remove columns with categorical variables
        val_cols = [n for n in range(data.shape[1]) if n not in cols]
        data = data[:, val_cols]
        return data