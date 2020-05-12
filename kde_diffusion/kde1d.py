"""
Kernel density estimation via diffusion for 1-dimensional input data.
"""
__license__ = 'MIT'


########################################
# Dependencies                         #
########################################
from numpy import array, arange
from numpy import exp, sqrt, pi as π
from numpy import ceil, log2
from numpy import product
from numpy import histogram
from scipy.fft import dct, idct
from scipy.optimize import brentq


########################################
# Main                                 #
########################################

def kde1d(x, n=1024, limits=None):
    """
    Estimates the 1d density from discrete observations x.

    The input is a list/array `x` of numbers that represent discrete
    observations of a random variable. They are binned on a grid of
    `n` points within the data `limits`, if specified, or within
    the limits given by the values' range. `n` will be coerced to the
    next power of two if it isn't one to begin with.

    The limits may be given as a tuple (`xmin`, `xmax`) or a single
    number denoting the upper bound of a range centered at zero.
    If any of those values are `None`, they will be inferred from the
    data.

    After binning, the function determines the optimal bandwidth
    according to the diffusion-based method. It then smooths the
    binned data over the grid using a Gaussian kernel with a standard
    deviation corresponding to that bandwidth.

    Returns the estimated `density` and the `grid` upon which it was
    computed, as well as the optimal `bandwidth` value the algorithm
    determined. Raises `ValueError` if the algorithm did not converge.
    """

    # Convert to array in case a list is passed in.
    x = array(x)

    # Round up the number of bins to the next power of 2.
    n = int(2**ceil(log2(n)))

    # Determine missing data limits.
    if limits is None:
        xmin = xmax = None
    elif isinstance(limits, tuple):
        (xmin, xmax) = limits
    else:
        xmin = -limits
        xmax = +limits
    if None in (xmin, xmax):
        delta = x.max() - x.min()
        if xmin is None:
            xmin = x.min() - delta/10
        if xmax is None:
            xmax = x.max() + delta/10

    # Determine the data range, required for scaling.
    Δx = xmax - xmin

    # Determine the number of data points.
    N = len(x)

    # Bin the samples on a regular grid.
    (binned, edges) = histogram(x, bins=n, range=(xmin, xmax))
    grid = edges[:-1]

    # Compute the 2d discrete cosine transform.
    transformed = dct(binned/N)
    transformed[0] /= 2

    # Pre-compute squared indices and transform before solver loop.
    k  = arange(n, dtype='float')
    k2 = k**2
    a2 = (transformed/2)**2

    # Define internal function to be solved iteratively.
    def ξγ(t, l=7):
        """Returns ξ γ^[l] as a function of diffusion time t."""
        f = 2*π**(2*l) * sum(k2**l * a2 * exp(-π**2 * k2*t))
        for s in range(l-1, 1, -1):
            K = product(range(1, 2*s, 2)) / sqrt(2*π)
            C = (1 + (1/2)**(s+1/2)) / 3
            t = (2*C*K/N/f)**(2/(3+2*s))
            f = 2*π**(2*s) * sum(k2**s * a2 * exp(-π**2 * k2*t))
        return (2*N*sqrt(π)*f)**(-2/5)

    # Solve for optimal diffusion time t*.
    try:
        ts = brentq(lambda t: t - ξγ(t), 0, 0.1)
    except ValueError:
        raise ValueError('Bandwidth optimization did not converge.') from None

    # Apply the Gaussian filter with the optimized kernel.
    smoothed = transformed * exp(-π**2 * ts/2 * k**2)

    # Reverse the transformation.
    smoothed[0] *= 2
    inverse = idct(smoothed)

    # Normalize the density.
    density = inverse * n/Δx

    # Determine bandwidth from diffusion time.
    bandwidth = sqrt(ts) * Δx

    # Return results.
    return (density, grid, bandwidth)
