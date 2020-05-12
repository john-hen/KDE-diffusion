"""
Reproduces the exact results as the reference implementation.
"""
__license__ = 'MIT'


########################################
# Dependencies                         #
########################################
from numpy import arange
from numpy import exp, sqrt
from numpy import pi as π
from numpy import zeros
from numpy import real
from numpy import hstack
from numpy import product
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

# Parameters for data generation and evaluation.
N = 1000
l = 5
n = 256
xmin = -l
xmax = +l

# Load intermediate data from the Matlab reference implementation.
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

# Determine data limits if none given.
if None in (xmin, xmax):
    delta = x.max() - x.min()
    if xmin is None:
        xmin = x.min() - delta/10
    if xmax is None:
        xmax = x.max() + delta/10

# Determine the data range, required for scaling.
Δx = xmax - xmin

# Determine the number of unique data points.
N = len(unique(x))

# Bin the samples on a regular grid.
(binned, edges) = histogram(x, bins=n, range=(xmin, xmax+Δx/(n-1)))
grid = edges[:-1]
assert isclose(grid, ref['xmesh']).all()
assert isclose(binned/N, ref['initial_data']).all()

# Compute the 2d discrete cosine transform.
transformed = dct1d(binned/N)
assert isclose(transformed, ref['a']).all()

# Pre-compute squared indices and transform before solver loop.
k  = arange(n, dtype='float')
k2 = k[1:]**2
a2 = (transformed[1:]/2)**2
assert isclose(k2, ref['I']).all()
assert isclose(a2, ref['a2']).all()

# Solve for optimal diffusion time t*.

def ξγ(t, l=7):
    f = 2*π**(2*l) * sum(k2**l * a2 * exp(-π**2 * k2*t))
    for s in range(l-1, 1, -1):
        K = product(range(1, 2*s, 2)) / sqrt(2*π)
        C = (1 + (1/2)**(s+1/2)) / 3
        t = (2*C*K/N/f)**(2/(3+2*s))
        f = 2*π**(2*s) * sum(k2**s * a2 * exp(-π**2 * k2*t))
    return (2*N*sqrt(π)*f)**(-2/5)

ts = brentq(lambda t: t - ξγ(t), 0, 0.1)

# Apply the Gaussian filter with the optimized kernel.
smoothed = transformed * exp(-π**2 * ts/2 * k**2)
assert isclose(smoothed, ref['a_t']).all()

# Reverse the transformation.
inverse = idct1d(smoothed)

# Normalize the density.
density = inverse / Δx
assert isclose(density, ref['density']).all()

# Determine bandwidth from diffusion time.
bandwidth = sqrt(ts) * Δx
assert isclose(bandwidth, ref['bandwidth'])
