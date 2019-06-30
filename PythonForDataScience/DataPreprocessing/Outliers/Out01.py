import numpy as np
from scipy import stats

threshold = 3


# region =========== Standard Deviation Method ==================
def StdDev_Method(inputDF):
    """
    Uses the **Standard deviation method** to filters all the outliers.
    Use this method if you only need the filtered dataset without any outliers.
    :param inputDF: DataFrame which contains the data to remove the outliers.
    :return: DataFrame with only inliers.
    """
    return inputDF[((inputDF - inputDF.mean()).abs() <= threshold * inputDF.std()).all(axis = 1)]


def StdDev_Method_With_Inliers(inputDF):
    """
    Uses the **Standard deviation method** to detect and mask all the outliers.
    Use this method if you need the dataset with both inliers and outliers.
    :param inputDF: DataFrame which contains the data to remove the outliers.
    :return: Detects the Outliers and returns the dataframe with boolean values, for each row.
    """
    return inputDF[((inputDF - inputDF.mean()).abs() > threshold * inputDF.std()).isnull().any(1)]


# endregion

# region =========== ZScore method for detecting outliers ==================
def ZScore_Method(inputDF):
    """
    Filters all the outliers using the **ZScore Method**.
    Use this method if you only need the filtered dataset without any outliers.
    :param inputDF: DataFrame which contains the data to remove the outliers.
    :return: DataFrame with only inliers
    """
    return inputDF[(np.abs(stats.zscore(inputDF)) < threshold).all(axis = 1)]


def ZScore_Method_With_Inliers(inputDF):
    """
    Using the **ZScore Method** to detect and mask all the entire dataframe with boolean values.
    Use this method if you need the dataset with both inliers and outliers.
    :param inputDF: DataFrame which contains the data to remove the outliers.
    :return: Detects the Outliers and returns the dataframe with boolean values, for each row.
    """
    return inputDF[(np.abs(stats.zscore(inputDF)) < threshold).all(axis = 1)]

# inputDF = 0
# mean_y = np.mean(inputDF)
# stdev_y = np.std(inputDF)
# z_scores = [(y - mean_y) / stdev_y for y in inputDF]
# return np.where(np.abs(z_scores) > threshold)

# endregion

# region =========== IQR Method for detecting outliers ==================

def IQR_Method(inputDF):
    """
    Filters all the outliers using the **IQR Method**.
    Use this method if you only need the filtered dataset without any outliers.
    :param inputDF: DataFrame which contains the data to remove the outliers.
    :return: DataFrame with only inliers
    """
    return inputDF[((inputDF >= (inputDF.quantile(.25) - (1.5 * (inputDF.quantile(.75) - inputDF.quantile(.25))))) & (inputDF <= (inputDF.quantile(.75) + (1.5 * (inputDF.quantile(.75) - inputDF.quantile(.25)))))).all(axis = 1)]


def IQR_Method_With_Inliers(inputDF):
    """
    Using the **IQR Method** to detect and mask all the entire dataframe with boolean values.
    Use this method if you need the dataset with both inliers and outliers.
    :param inputDF: DataFrame which contains the data to remove the outliers.
    :return: Detects the Outliers and returns the dataframe with boolean values, for each row.
    """
    return inputDF.mask(~((inputDF >= (inputDF.quantile(.25) - (1.5 * (inputDF.quantile(.75) - inputDF.quantile(.25))))) & (inputDF <= (inputDF.quantile(.75) + (1.5 * (inputDF.quantile(.75) - inputDF.quantile(.25))))))).isnull()

# quartile_1, quartile_3 = np.percentile(inputDF, [25, 75])
# iqr = quartile_3 - quartile_1
# lower_bound = quartile_1 - (iqr * 1.5)
# upper_bound = quartile_3 + (iqr * 1.5)
# return np.where((inputDF > upper_bound) | (inputDF < lower_bound))

# endregion

