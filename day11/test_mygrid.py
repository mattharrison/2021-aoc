import mygrid

import pytest

@pytest.fixture
def data():
    values = [[0,1,2],[3,4,5]] # 1
    return values

@pytest.fixture
def grid(data):
    return mygrid.Grid(data)

def test_grid(grid):
    assert grid.shape == (3,2)  # 3

def test_grid_iter(grid):
    res = list(grid)
    assert len(res) == 6

def test_grid_around(grid):
    res = list(grid.around(mygrid.Point(1,1, None)))
    assert len(res) == 5

def test_parse():
    res = mygrid.parse_txt(mygrid.SAMPLE)
    assert len(res) == 10

def test_step1():
    g = mygrid.parse_txt(mygrid.SMALL)
    new_grid, res = mygrid.part1_step(g)
    assert repr(new_grid) == ''
