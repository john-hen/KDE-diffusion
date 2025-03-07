# Implementation

This Python library was developed based on the existing Matlab
implementation for [1d][kde1d] and [2d][kde2d], which was used as the
primary reference (albeit possibly in earlier versions previously
stored at the same locations), and the [original paper][paper] as a
secondary source, mostly to understand the nomenclature and general
idea behind the method.

The Matlab implementation was first rewritten in Python to give the
exact same result, including intermediate steps, for the same test
case: a univariate normal sampling. See the [`verification`][verif]
folder in the source-code [repository][repo] for details.

Subsequently, the Python code was refactored in order to blend in
better with the existing software ecosystem, namely by leveraging
SciPy's forward and backward discrete cosine transformation for one
or n dimensions, [`dct`](#scipy.fft.dct)/[`dctn`](#scipy.fft.dctn)
and [`idct`](#scipy.fft.idct)/[`idctn`](#scipy.fft.idctn),
as well as NumPy's [`histogram`](#numpy.histogram) and
[`histogram2d`](#numpy.histogram2d), instead of the custom versions
the Matlab reference employs.

The reference uses a cosine transformation with a weight for the very
first component that is different from the one in any of the four types
of the transformation supported by SciPy. There is an easy work-around
for that, which is used in the current code. It should however be
possible to rewrite the algorithm in a more elegant way, one that avoids
the work-around altogether.

The Matlab implementation also bins the data somewhat differently in
1d vs. the 2d case. This minor inconsistency was removed. The change
is arguably insignificant as far as the final results are concerned,
but is a deviation nonetheless. In practical use, based on a handful
of tests, both implementations yield indiscernible results.

The 2d density is returned in matrix index order, also known as
Cartesian indexing, in which the first index (the matrix row) refers
to the x-coordinate and the second index (the matrix column) to y.
This is consistent with results returned by other kernel density
estimations, such as SciPy's, as well as NumPy's 2d-histogram function.
When saving or displaying the 2d density as an image, a different
memory layout is expected and the index order has to be reversed: y
before x. This comes down to a simple transposition, i.e. adding
[`.T`](#numpy.ndarray.T) in the code.

In very broad strokes, the method is this:
* Bin the data on a regular grid.
* Transform to Fourier space.
* This leaves Gaussian kernels intact.
* Gaussians are also elementary solutions to the diffusion equation.
* Leverage this to define condition for optimal smoothing.
* Find optimum by iteration in Fourier space.
* Smooth transformed data with optimized Gaussian kernel.
* Reverse transformation to obtain density estimation.


[kde1d]:   https://mathworks.com/matlabcentral/fileexchange/14034
[kde2d]:   https://mathworks.com/matlabcentral/fileexchange/17204
[paper]:   https://dx.doi.org/10.1214/10-AOS799
[verif]:   https://github.com/john-hen/KDE-diffusion/tree/main/verification
[repo]:    https://github.com/john-hen/kde-diffusion
