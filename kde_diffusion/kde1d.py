"""Kernel density estimation via diffusion for 1-dimensional data."""
__license__ = 'MIT'


########################################
# Dependencies                         #
########################################
import numpy as np
import sys
from numpy import pi as π

from scipy.optimize import brentq


########################################
# Main                                 #
########################################

def kde1d(x, n=2**14, limits=None):
    """
    Estimates the 1d density from discrete observations.

    The input is a list/array `x` of numbers that represent discrete
    observations of a random variable. They are binned on a grid of
    `n` points within the data `limits`, if specified, or within
    the limits given by the values' range. `n` will be coerced to the
    next highest power of two if it isn't one to begin with.

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
    x = np.array(x)

    # Round up number of bins to next power of two.
    n = int(2**np.ceil(np.log2(n)))

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
            xmin = x.min() - delta / 2
        if xmax is None:
            xmax = x.max() + delta / 2

    # Determine data range, required for scaling.
    Δx = xmax - xmin

    # Determine number of data points.
    N = len(x)

    # Bin samples on regular grid
    step = Δx / (n - 1)
    xmesh = xmin + np.arange(start=0, stop=Δx+step, step=step, dtype=float)
    binned, _ = histc(x, xmesh)
    binned = binned / binned.sum()

    # Compute 2d discrete cosine transform, then adjust first component.
    transformed = dct1d(binned)

    # Pre-compute squared indices and transform components before solver loop.
    k  = np.arange(0, n, dtype='float')      # "float" avoids integer overflow.
    k2 = k**2
    a2 = (transformed[1:]/2)**2
    k12 = k2[1:]

    # Define internal function to be solved iteratively.
    def ξγ(t, l=7):
        """Returns ξ γ^[l] as a function of diffusion time t."""
        f = 2*π**(2*l) * sum(k12**l * a2 * np.exp(-π**2 * k12*t))
        for s in range(l-1, 1, -1):
            K = np.product(range(1, 2*s, 2)) / np.sqrt(2*π)
            C = (1 + (1/2)**(s+1/2)) / 3
            t = (2*C*K/N/f)**(2/(3+2*s))
            f = 2*π**(2*s) * sum(k12**s * a2 * np.exp(-π**2 * k12*t))
        out = (2*N*np.sqrt(π)*f)**(-2/5)
        return out

    # Solve for optimal diffusion time t*.
    try:
        ts = brentq(lambda t: t - ξγ(t), 0, 0.1)
    except ValueError:
        raise ValueError('Bandwidth optimization did not converge.') from None

    # Apply Gaussian filter with optimized kernel.
    smoothed = transformed * np.exp(-π**2 * ts/2 * k2)

    # Reverse transformation after adjusting first component.
    inverse = idct1d(smoothed)

    # Normalize density.
    density = inverse / Δx

    # Determine bandwidth from diffusion time.
    bandwidth = np.sqrt(ts) * Δx

    # Return results.
    return (density, xmesh, bandwidth)



def idct1d(data):
    """
    # function out = idct1d(data)
    # % computes the inverse discrete cosine transform
    # [nrows, ~]=size(data);
    # % Compute weights
    # weights = nrows*exp(1i*(0:nrows-1)*pi/(2*nrows)).';
    # % Compute x tilde using equation (5.93) in Jain
    # data = real(ifft(weights.*data));
    # % Re-order elements of each column according to equations (5.93) and
    # % (5.94) in Jain
    # out = zeros(nrows,1);
    # out(1:2:nrows) = data(1:nrows/2);
    # out(2:2:nrows) = data(nrows:-1:nrows/2+1);
    # %   Reference:
    # %      A. K. Jain, "Fundamentals of Digital Image
    # %      Processing", pp. 150-153.
    # end
    """
    nrows = data.shape[0]
    seq = np.arange(nrows, dtype='float')
    weights = nrows * np.exp(1j * seq * π / (2 * nrows))
    wdata = np.multiply(weights, data)
    cdata = np.fft.ifft(wdata)
    rdata = cdata.real
    out = np.zeros(nrows)
    out[0:nrows-2:2] = rdata[0:int(nrows/2)-1]
    out[1:nrows-2:2] = rdata[nrows-1:int(nrows/2):-1]
    return out


def dct1d(data):
    """
    # % computes the discrete cosine transform of the column vector data
    # [nrows, ~]= size(data);
    # % Compute weights to multiply DFT coefficients
    # weight = [1;2*(exp(-1i*(1:nrows-1)*pi/(2*nrows))).'];
    # % Re-order the elements of the columns of x
    # data = [data(1:2:end,:); data(end:-2:2,:)];
    # % Multiply FFT by weights:
    # data= real(weight.* fft(data));
    """
    nrows = data.shape[0]
    weights = np.zeros(nrows, dtype=complex)
    seq = np.arange(1, nrows, dtype='float')
    weights[1:] = 2 * np.exp(-1j * seq * π / (2 * nrows))
    weights[0] = 1
    rdata = np.zeros(nrows)
    rdata[0:int(nrows/2)-1] = data[0:nrows-2:2]
    rdata[nrows-1:int(nrows/2):-1] = data[1:nrows-2:2]
    out = np.fft.fft(rdata)
    out = np.multiply(out, weights)
    out = out.real
    return out


def histc(X, bins):
    map_to_bins = np.digitize(X,bins)
    r = np.zeros(bins.shape)
    for i in map_to_bins:
        r[i-1] += 1
    return [r, map_to_bins]