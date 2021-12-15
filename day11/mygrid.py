from typing import List, Generator


class Point:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __repr__(self):
        return f'Point({self.x}, {self.y}, {self.value})'


class Grid:
    def __init__(self, data: List[List[object]]):
        self.rows = []
        for y, row in enumerate(data):
            this_row = []
            for x, value in enumerate(row):
                this_row.append(Point(x,y,value))
            self.rows.append(this_row)
        self.shape = (len(data[0]), len(data))

    def __repr__(self):
        lines = []
        for row in self.rows:
            lines.append(''.join(str(p.value) for p in row))
        return '\n'.join(lines)

    def __iter__(self):
        for row in self.rows:
            for point in row:
                yield point

    def copy(self):
        data = [[point.value for point in row]
                for row in self.rows]
        return self.__class__(data)

    def around(self, point: Point, include_diagonals=True) :
        deltas = [(0,1),(1,0),(0,-1),(-1,0)]
        if include_diagonals:
            deltas.extend([(1,1), (1,-1), (-1,-1), (-1, 1)])
        for delta_x, delta_y in deltas:
            # delta_x = delta[0]
            # delta_y = delta[1]
            x = point.x + delta_x
            y = point.y + delta_y
            if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
                yield self.rows[y][x]

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

SMALL = '''11111
19991
19191
19991
11111
'''

def part1_step(grid):
    """
    >>> g = parse_txt(SMALL)
    >>> part1_step(g)
    """
    next_grid = grid.copy()
    for point in next_grid:
        point.value += 1
        point.flashed = False
    done = False
    while not done:
        gt9 = [pt for pt in next_grid
               if pt.value > 9 and not pt.flashed]
        for pt in gt9:
            pt.flashed = True
            pt.value = 0
            for other in next_grid.around(pt):
                if not other.flashed:
                    other.value += 1
        done = len(gt9) == 0
    return next_grid, sum(pt.flashed for pt in next_grid)


def part1_step_old(grid):
    """
    >>> g = parse_txt(SMALL)
    >>> part1_step(g)
    """
    next_grid = grid.copy()
    for point in next_grid:
        point.value += 1
        point.flashed = False
    done = False
    while not done:
        done = True
        for pt in next_grid:
            if pt.value >= 10 and not pt.flashed:
                done = False
                pt.flashed = True
                for other in next_grid.around(pt):
                    if other.value >= 10 and not other.flashed:
                        other.flashed = True
                    other.value += 1

    for point in next_grid:
        if point.value > 9:
            point.value = 0
    
    return next_grid, sum(pt.flashed for pt in next_grid)




def parse_txt(txt):
    data = []
    for line in txt.strip().split('\n'):
        row = []
        for char in line:
            row.append(int(char))
        data.append(row)
    return Grid(data)

def part1(txt):
    ...

if __name__ == '__main__':
    import doctest
    doctest.testmod()

