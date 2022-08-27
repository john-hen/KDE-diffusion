"""Demonstrates that refactoring barely affected 1d result."""


########################################
# Dependencies                         #
########################################
from numpy import arange
from numpy import exp, sqrt
from numpy import pi as π
from numpy import product
from numpy import histogram
from scipy.fft import dct, idct
from scipy.optimize import brentq
from scipy.io import loadmat
from pathlib import Path
from matplotlib import pyplot


########################################
# Main                                 #
########################################

# Parameters from data generation and for evaluation.
N = 1000
l = 5
n = 256
xmin = -l
xmax = +l

# Load intermediate data from Matlab reference.
here = Path(__file__).parent
ref = loadmat(here/'kde1d.mat')
for (key, value) in ref.items():
    if hasattr(value, 'shape'):
        ref[key] = value.squeeze()
x = ref['data']
assert N == ref['N']
assert N == len(x)
assert n == ref['n']
assert n == len(ref['density'])

# Determine data range, required for scaling.
Δx = xmax - xmin

# Determine number of data points.
N = len(x)

# Bin samples on regular grid.
(binned, edges) = histogram(x, bins=n, range=(xmin, xmax))
grid = edges[:-1]

# Compute 2d discrete cosine transform. Adjust first component.
transformed = dct(binned/N)
transformed[0] /= 2

# Pre-compute squared indices and transform components before solver loop.
k  = arange(n, dtype='float')
k2 = k**2
a2 = (transformed/2)**2


# Define internal function to be solved iteratively.
def ξγ(t, l=7):
    f = 2*π**(2*l) * sum(k2**l * a2 * exp(-π**2 * k2*t))
    for s in range(l-1, 1, -1):
        K = product(range(1, 2*s, 2)) / sqrt(2*π)
        C = (1 + (1/2)**(s+1/2)) / 3
        t = (2*C*K/N/f)**(2/(3+2*s))
        f = 2*π**(2*s) * sum(k2**s * a2 * exp(-π**2 * k2*t))
    return (2*N*sqrt(π)*f)**(-2/5)


# Solve for optimal diffusion time t*.
ts = brentq(lambda t: t - ξγ(t), 0, 0.1)

# Apply Gaussian filter with optimized kernel.
smoothed = transformed * exp(-π**2 * ts/2 * k**2)

# Reverse transformation.
smoothed[0] *= 2
inverse = idct(smoothed)

# Normalize density.
density = inverse * n/Δx

# Determine bandwidth from diffusion time.
bandwidth = sqrt(ts) * Δx

# Plot (slightly different) density versus reference.
figure = pyplot.figure()
axes = figure.add_subplot()
axes.grid()
axes.plot(ref['density'])
axes.plot(density)
pyplot.show()
