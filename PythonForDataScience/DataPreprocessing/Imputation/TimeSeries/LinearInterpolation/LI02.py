"""

Interpolation (scipy.interpolate) -> 1-D interpolation (interp1d)
---------------------------------
There are several general interpolation methods available in SciPy, for data in 1, 2, and higher dimensions.
In this sample, we will look at a class representing **interpolant (interp1d)** in 1-D, offering several interpolation methods.

The interp1d class in scipy.interpolate is a convenient method to create a function based on fixed data points which can be evaluated anywhere within the domain defined by the given data using linear interpolation.

**scipy.interpolate.interp1d(x, y, kind='linear', axis=-1, copy=True, bounds_error=None, fill_value=nan, assume_sorted=False)**
**Note** that calling interp1d with NaNs present in input values results in undefined behaviour.

Parameters:
    x(N,)       : array_like. A 1-D array of real values.
    y(…,N,…)    : array_like. A N-D array of real values. The length of y along the interpolation axis must be equal to the length of x.
    kind        : str or int, optional.
                    Specifies the kind of interpolation as a string. viz ‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, ‘next’, where
                        ‘zero’, ‘slinear’, ‘quadratic’ and ‘cubic’ refer to a spline interpolation of zeroth, first, second or third order;
                    ‘previous’ and ‘next’ simply return the previous or next value of the point) or as an integer specifying the order of the spline interpolator to use.
                    Default is ‘linear’.
    axis        : int, optional. Specifies the axis of y along which to interpolate. Interpolation defaults to the last axis of y.
    copy        : bool, optional. If True, the class makes internal copies of x and y. If False, references to x and y are used. The default is to copy.
    bounds_error: bool, optional.
                    If True, a ValueError is raised any time interpolation is attempted on a value outside of the range of x (where extrapolation is necessary).
                    If False, out of bounds values are assigned fill_value. By default, an error is raised unless fill_value="extrapolate".
    fill_value  : array-like or (array-like, array_like) or “extrapolate”, optional.
                    - if a ndarray (or float), this value will be used to fill in for requested points outside of the data range.
                        If not provided, then the default is NaN. The array-like must broadcast properly to the dimensions of the non-interpolation axes.
                    - If a two-element tuple, then the first element is used as a fill value for x_new < x[0] and the second element is used for x_new > x[-1].
                        Anything that is not a 2-element tuple (e.g., list or ndarray, regardless of shape) is taken to be a single array-like argument
                        meant to be used for both bounds as below, above = fill_value, fill_value. New in version 0.17.0.
                    - If “extrapolate”, then points outside the data range will be extrapolated. New in version 0.17.0.
    assume_sorted: bool, optional. If False, values of x can be in any order and they are sorted first.
                    If True, x has to be an array of monotonically increasing values.

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Usage:
# An instance of this class is created by passing the 1-d vectors comprising the data.
# The instance of this class defines a __call__ method and can therefore by treated like a function which
# interpolates between known data values to obtain unknown values (it also has a docstring for help).
# Behavior at the boundary can be specified at instantiation time.

# Example 01: The following example shows how to use it to interpolate a 1 dimensional array.
x = np.arange(0, 10)
y = np.exp(-x/3.0)
f = interp1d(x, y)  # creating an instance.

xnew = np.arange(0, 9, 0.1)
ynew = f(xnew)   # use the instance (interpolation function) returned by `interp1d`
plt.plot(x, y, 'o', xnew, ynew, '-')
plt.show()

# Example 02: The following example demonstrates its use, for linear and cubic spline interpolation.
x = np.linspace(0, 10, num=11, endpoint=True)
y = np.cos(-x**2/9.0)
f = interp1d(x, y)
f2 = interp1d(x, y, kind='cubic')

xnew = np.linspace(0, 10, num=41, endpoint=True)

plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()

# Example 03: Another set of interpolations in interp1d is nearest, previous, and next, where they return the nearest, previous, or next point along the x-axis.
# Nearest and next can be thought of as a special case of a causal interpolating filter.
# The following example demonstrates their use, using the same data as in the previous example.
f1 = interp1d(x, y, kind='nearest')
f2 = interp1d(x, y, kind='previous')
f3 = interp1d(x, y, kind='next')

xnew = np.linspace(0, 10, num=1001, endpoint=True)

plt.plot(x, y, 'o')
plt.plot(xnew, f1(xnew), '-', xnew, f2(xnew), '--', xnew, f3(xnew), ':')
plt.legend(['data', 'nearest', 'previous', 'next'], loc='best')
plt.show()
