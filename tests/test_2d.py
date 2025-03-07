"""Tests the 2d kernel density estimation."""

from kde_diffusion import kde2d
from pathlib       import Path
from numpy         import isclose, load
from pytest        import raises


reference = None


def setup_module():
    global reference
    here = Path(__file__).parent
    reference = load(here/'reference2d.npz')


def test_reference():
    x = reference['x']
    y = reference['y']
    N = reference['N']
    assert len(x) == N
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


def test_arguments():
    samples = [-2, -1, 0, +1, +2]
    (density, grid, bandwith) = kde2d(samples*5, samples*5, 16)
    assert len(grid[0]) == 16
    assert len(grid[1]) == 16
    assert isclose(grid[0].min(), -3.0)
    assert isclose(grid[0].max(), +2.625)
    assert isclose(grid[1].min(), -3.0)
    assert isclose(grid[1].max(), +2.625)
    (density, grid, bandwidth) = kde2d(samples*5, samples*5, 16, (2, None))
    assert isclose(grid[0].min(), -2)
    assert isclose(grid[0].max(), +1.75)
    assert isclose(grid[1].min(), -3)
    assert isclose(grid[1].max(), +2.625)
    (density, grid, bandwidth) = kde2d(samples*5, samples*5, 16, (None, 2))
    assert isclose(grid[0].min(), -3)
    assert isclose(grid[0].max(), +2.625)
    assert isclose(grid[1].min(), -2)
    assert isclose(grid[1].max(), +1.75)
    (density, grid, bandwidth) = kde2d(samples*5, samples*5, 16, 2)
    assert isclose(grid[0].min(), -2)
    assert isclose(grid[0].max(), +1.75)
    assert isclose(grid[1].min(), -2)
    assert isclose(grid[1].max(), +1.75)
    with raises(ValueError):
        kde2d(samples, samples*2, 16)
    with raises(ValueError):
        kde2d(samples, samples, 16)
