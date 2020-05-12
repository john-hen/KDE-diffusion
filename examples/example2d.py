"""
Code example for two-dimensional input data.
"""
__license__ = 'MIT'


# Sample data points from a normal distribution.
from numpy.random import normal
x = normal(size=1000)
y = normal(size=1000)

# Estimate the density within +/- 5 standard deviations.
from kde_diffusion import kde2d
(density, grid, bandwidth) = kde2d(x, y, n=256, limits=5)

# Display the estimated density as an image.
from matplotlib import pyplot
figure = pyplot.figure()
axes = figure.add_subplot()
axes.imshow(density.T)
pyplot.show()
