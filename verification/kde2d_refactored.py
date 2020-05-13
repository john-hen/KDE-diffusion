"""
Demonstrates that refactoring did not affect 2d result.
"""
__license__ = 'MIT'


########################################
# Dependencies                         #
########################################
from numpy import array, arange, ones
from numpy import exp, sqrt, pi as π
from numpy import product, outer
from numpy import histogram2d
from numpy import isclose
from scipy.fft import dctn, idctn
from scipy.optimize import brentq
from scipy.io import loadmat
from pathlib import Path


########################################
# Main                                 #
########################################

# Parameters from data generation and for evaluation.
N = 1000
l = 5
n = 256
xmin = -l
xmax = +l
ymin = -l
ymax = +l

# Load intermediate data from Matlab reference.
here = Path(__file__).parent
ref = loadmat(here/'kde2d.mat')
for (key, value) in ref.items():
    if hasattr(value, 'shape'):
        ref[key] = value.squeeze()
x = ref['data'][:, 0]
y = ref['data'][:, 1]
assert N == ref['N']
assert N == len(x)
assert n == ref['n']
assert n == ref['density'].shape[0]

# Determine data ranges, required for scaling.
Δx = xmax - xmin
Δy = ymax - ymin

# Bin samples on regular grid.
(binned, xedges, yedges) = histogram2d(x, y, bins=n,
                                       range=((xmin, xmax), (ymin, ymax)))
assert isclose(binned/N, ref['initial_data']).all()

# Compute 2d discrete cosine transform.
transformed = dctn(binned/N)
transformed[0, :] /= 2
transformed[:, 0] /= 2
assert isclose(transformed, ref['a']).all()

# Pre-compute squared indices and transform components before solver loop.
k  = arange(n, dtype='float')          # float avoids integer overflow.
k2 = k**2
a2 = transformed**2

# Define internal functions to be solved iteratively.
def γ(t):
    Σ = ψ(0, 2, t) + ψ(2, 0, t) + 2*ψ(1, 1, t)
    γ = (2*π*N*Σ)**(-1/3)
    return (t - γ) / γ

def ψ(i, j, t):
    if i + j <= 4:
        Σψ = ψ(i+1, j, t) + ψ(i, j+1, t)
        C  = (1 + 1/2**(i+j+1)) / 3
        Πi = product(arange(1, 2*i, 2))
        Πj = product(arange(1, 2*j, 2))
        t  = (C*Πi*Πj / (π*N*abs(Σψ))) ** (1/(2+i+j))
    w = 0.5 * ones(n)
    w[0] = 1
    w = w * exp(-π**2 * k2*t)
    wx = w * k2**i
    wy = w * k2**j
    return (-1)**(i+j) * π**(2*(i+j)) * wy @ a2 @ wx

# Solve for optimal diffusion time t*.
ts = brentq(lambda t: t - γ(t), 0, 0.1)
assert isclose(ts, ref['t_star'])

# Calculate diffusion times along x- and y-axis.
ψ02 = ψ(0, 2, ts)
ψ20 = ψ(2, 0, ts)
ψ11 = ψ(1, 1, ts)
tx1 = (ψ02**(3/4) / (4*π*N*ψ20**(3/4) * (ψ11 + sqrt(ψ02*ψ20))) )**(1/3)
tx2 = (ψ20**(3/4) / (4*π*N*ψ02**(3/4) * (ψ11 + sqrt(ψ02*ψ20))) )**(1/3)

# Apply Gaussian filter with optimized kernel.
smoothed = transformed * outer(exp(-π**2 * k2 * tx2/2),
                               exp(-π**2 * k2 * tx1/2))
assert isclose(smoothed, ref['a_t']).all()

# Reverse transformation.
smoothed[0, :] *= 2
smoothed[:, 0] *= 2
inverse = idctn(smoothed)

# Normalize density.
density = inverse * n/Δx * n/Δy
assert isclose(density.T, ref['density']).all()

# Determine bandwidth from diffusion times.
bandwidth = array([sqrt(tx2)*Δx, sqrt(tx1)*Δy])
assert isclose(bandwidth, ref['bandwidth']).all()
