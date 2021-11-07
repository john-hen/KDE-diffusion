"""Code example for two-dimensional input data."""

# Sample data points from normal distribution.
from numpy.random import normal
x = normal(size=1000)
y = normal(size=1000)

# Estimate density within ±5 standard deviations.
from kde_diffusion import kde2d
(density, grid, bandwidth) = kde2d(x, y, n=256, limits=5)

# Display estimated density as image.
from matplotlib import pyplot
figure = pyplot.figure()
axes = figure.add_subplot()
axes.imshow(density.T)
pyplot.show()
