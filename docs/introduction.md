# Introduction

Kernel density estimation is a statistical method to infer the
*true* probability density function that governs the distribution of
a random variable from discrete observations of that same entity.
The variable may have more than one component, i.e. be described by
several coordinates.

An instructive, two-dimensional example is population density, which
is derived from discrete locations, such as people's home addresses
or animals encountered at specific places in the wild. A technical
use case is the determination of a spatially-resolved particle flux
as measured by a detector array that is sensitive to rare, individual
impacts.

Kernel density estimation basically works like this: Bin the discrete
observations in a histogram. This is straightforward and takes little
computation time. Then smooth the data over the bins/grid with an
image filter that adds *adequate* blur. The shape of the filter
function is referred to as the "kernel" and its spatial extent as the
"bandwidth". The trick is to find the optimal filter size, one that
does not smear out the data too much, but also averages over the
artifacts that are due to the discrete nature of the input.

This library provides the adaptive kernel density estimator based on
linear diffusion processes for one-dimensional and two-dimensional
input data as outlined in the [2010 paper by Botev et al.][paper] The
reference implementation for [1d] and [2d] was written in Matlab by
the paper's first author.

The diffusion-inspired method is particularly fast. Orders of magnitude
faster, for instance, than [SciPy's Gaussian kernel estimator][scipy].
Or those provided by [Scikit-Learn][sklearn]. And most of [KDEpy's] —
except for [`FFTKDE`][fftkde], which uses a very similar algorithm, but
has no automatic bandwidth selection in dimensions higher than one.

Automatic bandwidth selection is however key. Otherwise one may as well
just apply a [Gaussian filter][gfilter] and manually tune its size, i.e.
the bandwidth, until the results look pleasing to the human eye. The
bandwidth selection is what makes kernel density estimation a
non-parametric method, so that we avoid making — possibly misguided —
assumptions about the nature of the data.

[paper]:   https://dx.doi.org/10.1214/10-AOS799
[1d]:      https://mathworks.com/matlabcentral/fileexchange/14034
[2d]:      https://mathworks.com/matlabcentral/fileexchange/17204
[scipy]:   scipy:scipy.stats.gaussian_kde
[sklearn]: sklearn:sklearn.neighbors.KernelDensity
[gfilter]: scipy:scipy.ndimage.gaussian_filter
[KDEpy's]: https://kdepy.readthedocs.io
[fftkde]:  kdepy:KDEpy.FFTKDE.FFTKDE
