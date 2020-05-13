"""
Code example for one-dimensional input data.
"""
__license__ = 'MIT'

# Sample data points from normal distribution.
from numpy.random import normal
x = normal(size=1000)

# Estimate density within ±5 standard deviations.
from kde_diffusion import kde1d
(density, grid, bandwidth) = kde1d(x, n=256, limits=5)

# Calculate actual density on same grid.
from scipy.stats import norm
actual = norm.pdf(grid)

# Plot estimated and actual density.
from matplotlib import pyplot
figure = pyplot.figure()
axes = figure.add_subplot()
axes.plot(grid, density, label='estimated', linewidth=5, color='goldenrod')
axes.plot(grid, actual,  label='actual', linestyle='--', color='black')
axes.legend()
pyplot.show()
