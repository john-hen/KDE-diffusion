# KDE-diffusion

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
input data as outlined in the [2010 paper by Botev et al.][1] The
reference implementation for [1d][2] and [2d][3], in Matlab, was
provided by the paper's first author, Zdravko Botev. This is a
re-implementation in Python, with added test coverage.

The diffusion-inspired method is particularly fast. Orders of
magnitude faster, for instance, than [SciPy's Gaussian kernel
estimator][4]. Or those provided by [Scikit-Learn][5]. And most of
[KDEpy's][6] — except for `FFTKDE`, which uses a very similar
algorithm, but has no automatic bandwidth selection in dimensions
higher than one.

Automatic bandwidth selection is however key. Otherwise one may as
well just apply a [Gaussian filter][7] and manually tune its size,
i.e. the bandwidth, until the results look pleasing to the human eye.
The bandwidth selection is what makes kernel density estimation a
non-parametric method, so that we avoid making — possibly misguided —
assumptions about the nature of the data.


[1]: https://dx.doi.org/10.1214/10-AOS799
[2]: https://mathworks.com/matlabcentral/fileexchange/14034
[3]: https://mathworks.com/matlabcentral/fileexchange/17204
[4]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html
[5]: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KernelDensity.html
[6]: https://kdepy.readthedocs.io
[7]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter.html


```{toctree}
:hidden:

installation
usage
implementation
api
```
