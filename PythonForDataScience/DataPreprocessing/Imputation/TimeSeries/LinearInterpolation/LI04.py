"""
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html
https://www.geeksforgeeks.org/python-pandas-dataframe-interpolate/

pandas.DataFrame.interpolate
----------------------------
Pandas dataframe.interpolate() function is basically used to fill NA values in the dataframe or series.
But, this is a very powerful function to fill the missing values. It uses various interpolation technique to fill the missing values rather than hard-coding the value.

**DataFrame.interpolate(method='linear', axis=0, limit=None, inplace=False, limit_direction='forward', limit_area=None, downcast=None, **kwargs)**
    *Please note that only method='linear' is supported for DataFrame/Series with a MultiIndex.*

**Parameters:**
    - method : str, default ‘linear’. Interpolation technique to use. One of the following:
        - ‘linear’: Ignore the index and treat the values as equally spaced. This is the only method supported on MultiIndexes.
        - ‘time’: Works on daily and higher resolution data to interpolate given length of interval.
        - ‘index’, ‘values’: use the actual numerical values of the index.
        - ‘pad’: Fill in NaNs using existing values.
        - ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘spline’, ‘barycentric’, ‘polynomial’: Passed to scipy.interpolate.interp1d.
            Both ‘polynomial’ and ‘spline’ require that you also specify an order (int),
            e.g. df.interpolate(method='polynomial', order=4). These use the numerical values of the index.
        - ‘krogh’, ‘piecewise_polynomial’, ‘spline’, ‘pchip’, ‘akima’: Wrappers around the SciPy interpolation methods of similar names. See Notes.
        - ‘from_derivatives’: Refers to scipy.interpolate.BPoly.from_derivatives which replaces ‘piecewise_polynomial’ interpolation method in scipy 0.18.

        New in version 0.18.1: Added support for the ‘akima’ method.
        Added interpolate method ‘from_derivatives’ which replaces ‘piecewise_polynomial’ in SciPy 0.18;
        backwards-compatible with SciPy < 0.18

    - axis : {0 or ‘index’, 1 or ‘columns’, None}, default None. Axis to interpolate along.
    - limit : int, optional. Maximum number of consecutive NaNs to fill. Must be greater than 0.
    - inplace : bool, default False. Update the data in place if possible.
    - limit_direction : {‘forward’, ‘backward’, ‘both’}, default ‘forward’. If limit is specified, consecutive NaNs will be filled in this direction.
    - limit_area : {None, ‘inside’, ‘outside’}, default None. If limit is specified, consecutive NaNs will be filled with this restriction.
        - ‘None’: No fill restriction.
        - ‘inside’: Only fill NaNs surrounded by valid values (interpolate).
        - ‘outside’: Only fill NaNs outside valid values (extrapolate). New in version 0.21.0.

    - downcast : optional, ‘infer’ or None, defaults to None. Downcast dtypes if possible.
    -  **kwargs: Keyword arguments to pass on to the interpolating function.

**Returns:**
    Series or DataFrame
    Returns the same object type as the caller, interpolated at some or all NaN values

**Note:** *The ‘krogh’, ‘piecewise_polynomial’, ‘spline’, ‘pchip’ and ‘akima’ methods are wrappers around the respective SciPy implementations of similar names. These use the actual numerical values of the index. For more information on their behavior, see the SciPy documentation and SciPy tutorial.*
"""
import pandas as pd
import numpy as np

# Example 01: Filling in NaN in a Series via linear interpolation.
s = pd.Series([0, 1, np.nan, 3])
# 0    0.0
# 1    1.0
# 2    NaN
# 3    3.0
# dtype: float64
s.interpolate()
# 0    0.0
# 1    1.0
# 2    2.0
# 3    3.0
# dtype: float64

# Example 02: Filling in NaN in a Series by padding, but filling at most two consecutive NaN at a time.
s = pd.Series([np.nan, "single_one", np.nan,"fill_two_more", np.nan, np.nan, np.nan, 4.71, np.nan])
# 0              NaN
# 1       single_one
# 2              NaN
# 3    fill_two_more
# 4              NaN
# 5              NaN
# 6              NaN
# 7             4.71
# 8              NaN
# dtype: object
s.interpolate(method='pad', limit=2)
# 0              NaN
# 1       single_one
# 2       single_one
# 3    fill_two_more
# 4    fill_two_more
# 5    fill_two_more
# 6              NaN
# 7             4.71
# 8             4.71
# dtype: object

# Example 03: Filling in NaN in a Series via polynomial interpolation or splines: Both ‘polynomial’ and ‘spline’ methods require that you also specify an order (int).
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.interpolate.spline.html
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.interpolate.PPoly.html
s = pd.Series([0, 2, np.nan, 8])
s.interpolate(method='spline', order=2)
# 0    0.000000
# 1    2.000000
# 2    4.666667
# 3    8.000000
# dtype: float64

# Example 04: Fill the DataFrame forward (that is, going down) along each column using linear interpolation.
# Note how the last entry in column ‘a’ is interpolated differently, because there is no entry after it to use for interpolation.
# Note how the first entry in column ‘b’ remains NaN, because there is no entry befofe it to use for interpolation.
df = pd.DataFrame([(0.0,  np.nan, -1.0, 1.0),(np.nan, 2.0, np.nan, np.nan),(2.0, 3.0, np.nan, 9.0),(np.nan, 4.0, -4.0, 16.0)],columns=list('abcd'))
#      a    b    c     d
# 0  0.0  NaN -1.0   1.0
# 1  NaN  2.0  NaN   NaN
# 2  2.0  3.0  NaN   9.0
# 3  NaN  4.0 -4.0  16.0

df.interpolate(method='linear', limit_direction='forward', axis=0)
#      a    b    c     d
# 0  0.0  NaN -1.0   1.0
# 1  1.0  2.0 -2.0   5.0
# 2  2.0  3.0 -3.0   9.0
# 3  2.0  4.0 -4.0  16.0

# Example 05: Use interpolate() function to interpolate the missing values in the backward direction using linear method
#   and putting a limit on maximum number of consecutive Na values that could be filled.
df.interpolate(method ='linear', limit_direction ='backward', limit = 1)
# You can see that the last value in column a is not filled, since there is no entry after it to use.
# Since we have used the limit option, only one value is filled in column c.