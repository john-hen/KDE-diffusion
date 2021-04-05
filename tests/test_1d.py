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

def test_density():
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


########################################
# Main                                 #
########################################

if __name__ == '__main__':
    # Runs if test script is executed directly, and not via pytest.
    setup_module()
    test_density()
