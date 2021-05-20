"""Tests the 1d kernel density estimation."""
__license__ = 'MIT'


########################################
# Dependencies                         #
########################################
import parent # noqa F401
from kde_diffusion import kde1d
from pathlib import Path
from numpy import isclose, load


########################################
# Fixtures                             #
########################################
reference = None


def setup_module():
    global reference
    here = Path(__file__).parent
    reference = load(here/'reference1d.npz')


########################################
# Tests                                #
########################################

def test_reference():
    x = reference['x']
    N = reference['N']
    assert N == len(x)
    n = reference['n']
    xmin = reference['xmin']
    xmax = reference['xmax']
    (density, grid, bandwidth) = kde1d(x, n, (xmin, xmax))
    assert isclose(density, reference['density']).all()
    assert isclose(grid, reference['grid']).all()
    assert isclose(bandwidth, reference['bandwidth']).all()


def test_arguments():
    (density, grid, bandwidth) = kde1d([-2, -1, 0, +1, +2]*20, 4)
    assert len(grid) == 4
    assert isclose(grid.min(), -2.4)
    assert isclose(grid.max(), +1.2)
    (density, grid, bandwidth) = kde1d([-2, -1, 0, +1, +2]*20, 4, 2)
    assert isclose(grid.min(), -2)
    assert isclose(grid.max(), +1)
    try:
        kde1d([-2, -1, 0, +1, +2]*10, 4)
        raised_error = False
    except ValueError:
        raised_error = True
    assert raised_error


########################################
# Main                                 #
########################################

if __name__ == '__main__':
    setup_module()
    test_reference()
    test_arguments()
