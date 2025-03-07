"""Reproduces exact same results as 1d reference implementation."""


########################################
# Dependencies                         #
########################################
from numpy import arange
from numpy import exp, sqrt
from numpy import pi as π
from numpy import zeros
from numpy import real
from numpy import hstack
from numpy import prod as product
from numpy import unique
from numpy import histogram
from numpy import isclose
from scipy.fft import fft, ifft
from scipy.optimize import brentq
from scipy.io import loadmat
from pathlib import Path


########################################
# Transforms                           #
########################################

def dct1d(data):
    n = len(data)
    weights = 2 * exp(-1j * arange(n) * π/(2*n))
    weights[0] = 1
    reordered = hstack((data[::2], data[::-2]))
    return real(weights * fft(reordered))


def idct1d(data):
    n = len(data)
    weights = n * exp(1j * arange(n) * π/(2*n))
    inverse = real(ifft(weights*data))
    reordered = zeros(n)
    half = int(n/2)
    reordered[0::2] = inverse[:half]
    reordered[1::2] = inverse[:half-1:-1]
    return reordered


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

# Determine number of unique data points.
N = len(unique(x))

# Bin samples on regular grid.
(binned, edges) = histogram(x, bins=n, range=(xmin, xmax+Δx/(n-1)))
grid = edges[:-1]
assert isclose(grid, ref['xmesh']).all()
assert isclose(binned/N, ref['initial_data']).all()

# Compute 2d discrete cosine transform.
transformed = dct1d(binned/N)
assert isclose(transformed, ref['a']).all()

# Pre-compute squared indices and transform components before solver loop.
k  = arange(n, dtype='float')
k2 = k[1:]**2
a2 = (transformed[1:]/2)**2
assert isclose(k2, ref['I']).all()
assert isclose(a2, ref['a2']).all()


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
assert isclose(smoothed, ref['a_t']).all()

# Reverse transformation.
inverse = idct1d(smoothed)

# Normalize density.
density = inverse / Δx
assert isclose(density, ref['density']).all()

# Determine bandwidth from diffusion time.
bandwidth = sqrt(ts) * Δx
assert isclose(bandwidth, ref['bandwidth'])
