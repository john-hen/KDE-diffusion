"""
Kernel density estimation via diffusion in 1d and 2d.

Provides the fast, adaptive kernel density estimator based on
linear diffusion processes for 1-dimensional and 2-dimensional
input data as outlined in the [2010 paper by Botev et al.][1]

The [reference implementation][2] in Matlab was provided by the
paper's first author, Zdravko Botev. This is a re-implementation
in Python with added test coverage.

[1]: http://dx.doi.org/10.1214/10-AOS799
[2]: https://mathworks.com/matlabcentral/fileexchange/17204
"""


# Meta information
__title__     = 'KDE-diffusion'
__synopsis__  = 'Kernel density estimation via diffusion.'
__version__   = '0.9'
__date__      = '2020–05–12'
__author__    = 'John Hennig'
__copyright__ = 'John Hennig'
__license__   = 'MIT'


# Public interface
from .kde1d import kde1d
from .kde2d import kde2d
