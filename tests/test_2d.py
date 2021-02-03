"""Tests the 2d kernel density estimation."""
__license__ = 'MIT'


########################################
# Dependencies                         #
########################################
import parent
from kde_diffusion import kde2d
from pathlib import Path
from numpy import isclose, load


########################################
# Fixtures                             #
########################################
reference = None

def setup_module():
    global reference
    here = Path(__file__).parent
    reference = load(here/'reference2d.npz')


########################################
# Test                                 #
########################################
def test_density():
    x = reference['x']
    y = reference['y']
    N = reference['N']
    assert N == len(x)
    n = reference['n']
    xmin = reference['xmin']
    xmax = reference['xmax']
    ymin = reference['ymin']
    ymax = reference['ymax']
    (density, grid, bandwidth) = kde2d(x, y, n, ((xmin, xmax), (ymin, ymax)))
    assert isclose(grid[0].min(), xmin)
    assert isclose(grid[0].max(), xmax - (xmax-xmin)/n)
    assert isclose(grid[1].min(), ymin)
    assert isclose(grid[1].max(), ymax - (ymax-ymin)/n)
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
