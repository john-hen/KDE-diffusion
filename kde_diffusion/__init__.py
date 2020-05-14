"""
Kernel density estimation via diffusion in 1d and 2d.

This module holds meta information and exposes the library's public
interface. The actual functionality is implemented in separate
modules.
"""

# Meta information
__title__     = 'KDE-diffusion'
__synopsis__  = 'Kernel density estimation via diffusion.'
__version__   = '1.0.0'
__date__      = '2020–05–14'
__author__    = 'John Hennig'
__copyright__ = 'John Hennig'
__license__   = 'MIT'

# Public interface
from .kde1d import kde1d
from .kde2d import kde2d
