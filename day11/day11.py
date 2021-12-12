import sys
sys.path.append('../gridder/')
from grid import Grid, Point


SAMPLE = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
'''

REAL = '''6636827465
6774248431
4227386366
7447452613
6223122545
2814388766
6615551144
4836235836
5334783256
4128344843
'''

def parse_txt(txt):
    """
    >>> print(parse_txt(SAMPLE))
      5   4   8   3   1   4   3   2   2   3
      2   7   4   5   8   5   4   7   1   1
      5   2   6   4   5   5   6   1   7   3
      6   1   4   1   3   3   6   1   4   6
      6   3   5   7   3   8   5   4   7   8
      4   1   6   7   5   2   4   6   4   5
      2   1   7   6   8   4   1   7   2   1
      6   8   8   2   8   8   1   1   3   4
      4   8   4   6   8   4   8   5   5   4
      5   2   8   3   7   5   1   5   2   6

    """
    lines = []
    for line in txt.strip().split('\n'):
        lines.append([int(v) for v in line])
    return Grid(lines)

BASIC = """11111
19991
19191
19991
11111
"""

def part1(txt):
    """
    >>> print(part1(SAMPLE))
    1656
      0   3   9   7   6   6   6   8   6   6
      0   7   4   9   7   6   6   9   1   8
      0   0   5   3   9   7   6   9   3   3
      0   0   0   4   2   9   7   8   2   2
      0   0   0   4   2   2   9   8   9   2
      0   0   5   3   2   2   2   8   7   7
      0   5   3   2   2   2   2   9   6   6
      9   3   2   2   2   2   8   9   6   6
      7   9   2   2   2   8   6   8   6   6
      6   7   8   9   9   9   8   7   6   6

    """
    g = parse_txt(txt)
    count_flashed = 0
    for step in range(100):
        g, flashed = part1_step(g)
        count_flashed += len(flashed)
    print(count_flashed)
    return g

def part2(txt):
    g = parse_txt(txt)
    grid_size = g.shape[0] * g.shape[1]

    for step in range(1, 1000):
        g, flashed = part1_step(g)
        print(step, len(flashed))
        if len(flashed) == grid_size:
            print(f'found {step}')
            break
    return g

def part1_step(grid):
    """
    >>> g= parse_txt(BASIC)
    >>> g, flashed = part1_step(g)
    >>> print(g)
      3   4   5   4   3
      4   0   0   0   4
      5   0   0   0   5
      4   0   0   0   4
      3   4   5   4   3
    """

    next_grid = grid.copy()
    next_grid.map(lambda pt: pt.value+1)
    done = False
    flashed = set()
    while not done:
        gt9 = [pt for pt in next_grid if pt.value > 9 and pt not in flashed]
        for pt in gt9:
            flashed.add(pt)
            pt.value = 0
            for neighbor in next_grid.around(pt):
                if neighbor not in flashed:
                    neighbor.value += 1
        done = len(gt9) == 0
    return next_grid, flashed


if __name__ == '__main__':
    import doctest
    #doctest.testmod()

    part1(SAMPLE)# 1656

    part1(REAL)#1585
    part2(SAMPLE)# 194
    part2(REAL)# 381
