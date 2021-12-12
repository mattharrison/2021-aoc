from pytest import fixture

from grid import Point, Grid

@fixture
def small_data():
    return [[1,2,3],[4,5,6]]

@fixture
def small_grid(small_data):
    return Grid(small_data)



def test_point():
    p = Point(1,1,'hello')
    assert p.x == 1


def test_point_hash():
    p = Point(1,1,'hello')
    h1 = hash(p)
    p.value = 'goodbye'
    h2 = hash(p)

    assert h1 == h2
    p2 = Point(1,1,'hello')
    assert h1 == hash(p2)
    assert h1 != hash(Point(0,1,'hello'))

def test_grid(small_grid):
    assert small_grid.shape == (3, 2)

def test_grid_iter(small_grid):
    points = list(small_grid)
    assert len(points) == 6
    assert points[0].x == 0
    assert points[0].y == 0
    assert points[-1].x == 2
    assert points[-1].y == 1

def test_around(small_grid):
    around = list(small_grid.around(Point(1,1,None)))
    assert {(p.x, p.y) for p in around} == {(0, 0), (0,1), (1,0), (2,0), (2, 1)}

def test_str(small_grid):
    res = str(small_grid)
    assert res == '  1   2   3\n  4   5   6'



