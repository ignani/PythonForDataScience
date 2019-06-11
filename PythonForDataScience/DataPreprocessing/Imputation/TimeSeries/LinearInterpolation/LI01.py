"""
https://www.numpy.org/devdocs/reference/generated/numpy.interp.html

numpy.interp
------------

numpy.interp(x, xp, fp, left=None, right=None, period=None)[source]
    One-dimensional linear interpolation.
    Returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x.

Parameters:
    x : array_like. The x-coordinates at which to evaluate the interpolated values.
    xp : 1-D sequence of floats. The x-coordinates of the data points, must be increasing if argument period is not specified.
        Otherwise, xp is internally sorted after normalizing the periodic boundaries with xp = xp % period.
    fp : 1-D sequence of float or complex. The y-coordinates of the data points, same length as xp.
    left : optional float or complex corresponding to fp. Value to return for x < xp[0], default is fp[0].
    right : optional float or complex corresponding to fp. Value to return for x > xp[-1], default is fp[-1].
    period : None or float, optional. A period for the x-coordinates.
        This parameter allows the proper interpolation of angular x-coordinates. Parameters left and right are ignored if period is specified.

Returns:
    y : float or complex (corresponding to fp) or ndarray. The interpolated values, same shape as x.

Raises:
    ValueError: If xp and fp have different length If xp or fp are not 1-D sequences If period == 0

"""
import numpy as np
import matplotlib.pyplot as plt

# Example 01: Simple interpolation of one data point at 2.5
xp = [1, 2, 3]
fp = [3, 2, 0]
np.interp(2.5, xp, fp)

# Example 02: Interpolation of multiple datapoints as specified in the array, passed as parameter x.
np.interp([0, 1, 1.5, 2.72, 3.14], xp, fp)

# Example 03: Interpolation using the "right" parameter.
UNDEF = -99.0
np.interp(3.14, xp, fp, right=UNDEF)

# Example 04: Interpolation of multiple data points & polting the same using matplotlib
x = np.linspace(0, 2*np.pi, 10)
y = np.sin(x)
xvals = np.linspace(0, 2*np.pi, 50)
yinterp = np.interp(xvals, x, y)

plt.plot(x, y, 'o')
plt.plot(xvals, yinterp, '-x')
plt.show()

# Example 05: Interpolation with periodic x co-ordinates.
x = [-180, -170, -185, 185, -10, -5, 0, 365]
xp = [190, -190, 350, -350]
fp = [5, 10, 3, 4]
np.interp(x, xp, fp, period=360)

# Example 06: Complex interpolation:
x = [1.5, 4.0]
xp = [2,3,5]
fp = [1.0j, 0, 2+3j]
np.interp(x, xp, fp)