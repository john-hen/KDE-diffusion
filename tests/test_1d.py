"""Tests the 1d kernel density estimation."""

from kde_diffusion import kde1d
from pathlib       import Path
from numpy         import isclose, load
from pytest        import raises


reference = None


def setup_module():
    global reference
    here = Path(__file__).parent
    reference = load(here/'reference1d.npz')


def test_reference():
    x = reference['x']
    N = reference['N']
    assert len(x) == N
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
    with raises(ValueError):
        kde1d([-2, -1, 0, +1, +2]*10, 4)
