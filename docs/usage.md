Usage
-----

Code example for one-dimensional input data:

```python
# Sample data points from a normal distribution.
from numpy.random import normal
x = normal(size=1000)

# Estimate the density within +/- 5 standard deviations.
from kde_diffusion import kde1d
(density, grid, bandwidth) = kde1d(x, n=256, limits=5)

# Calculate the actual density on the same grid.
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
```

Code example for two-dimensional input data:

```python
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
```

Note that the density is returned in matrix index order, also known as
Cartesian indexing, i.e. with the first index referring to the x-axis
and the second to the y-axis. This is the common convention for 2d
histograms and kernel density estimations, or science in general.
Images, however, are universally indexed the other way around: y before
x. This is why the density in the example is transposed before being
displayed.
