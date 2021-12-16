from dataclasses import dataclass, field
from os import nice
from re import split
import sys
sys.path.append('../gridder')
#import grid
from typing import List, Dict, Set

@dataclass(unsafe_hash=True)
class Point:
    x: int
    #x: int = field(hash=True)
    #y: int = field(hash=True)
    y: int
    value: object= field(hash=False)
    #value: object


class Grid:
    def __init__(self, data:List[List[object]], pt_class=Point):
        self.rows:List[List[Point]] =  []
        for y, row in enumerate(data):
            this_row = []
            for x, val in enumerate(row):
                this_row.append(pt_class(x,y,val))
            self.rows.append(this_row)
        self.shape = (len(data[0]), len(data))

    def __iter__(self): 
        for row in self.rows:
            yield from row

    def get(self, x:int, y:int) -> Point:
        return self.rows[y][x]

    def columns(self):
        for x in range(self.shape[0]):
            yield [self.rows[y][x] for y in range(self.shape[1])]

    def __str__(self):
        lines = []
        for row in self.rows:
            line = ' '.join([f'{pt.value:1}' for pt in row])
            lines.append(line)
        return '\n'.join(lines)

    def map(self, function):
        for point in self:
            point.value = function(point)

    def get_data(self):
        data = []
        for row in self.rows:
            data.append([p.value for p in row])
        return data

    def copy(self):
        return self.__class__(self.get_data())

    def around(self, point, include_diagonals=True):
        deltas = [(0,1), (1,0), (0,-1), (-1,0)]
        if include_diagonals:
            deltas.extend([(1,1), (1,-1), (-1,-1), (-1,1)])
        for delta_x, delta_y in deltas:
            x = point.x + delta_x
            y = point.y + delta_y
            if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
                yield self.rows[y][x]



SAMPLE = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''

def part1(txt):
    grid = parse_txt(txt)
    path = a_star(grid, grid.get(0,0), grid.get(grid.shape[0]-1, grid.shape[1]-1))
    path_grid = grid.copy()
    print(sum(pt.value for pt in path[1:]))
    for pt in path:
        path_grid.rows[pt.y][pt.x].value = '*'
    print(path_grid)
    print(path)

SMALL = '''123
987
'''

def part2(txt):
    grid = parse_txt_part2(txt)
    path = a_star(grid, grid.get(0,0), grid.get(grid.shape[0]-1, grid.shape[1]-1))
    path_grid = grid.copy()
    print('sum', sum(pt.value for pt in path[1:]))
    for pt in path:
        path_grid.rows[pt.y][pt.x].value = '*'
    # print(path_grid)
    #print(path)


def parse_txt_part2(txt:str):
    """
    >>> part2(SMALL)
    """
    numeric = [[int(char) for char in line]
               for line in txt.strip().split('\n') ]
    len_rows = len(numeric)
    len_cols = len(numeric[0])
    # add rows
    for i in range(4):
        for row in range(len_rows):
            numeric.append([val+1 if val <= 8 else 1
                            for val in numeric[len(numeric)-len_rows]])
    # add columns
    new_rows = []
    for row in numeric:
        new_rows.append(repeat_loop(row, 4))

    return Grid(new_rows)

def repeat_loop(vals, repeat_n):
    """
    >>> #repeat_loop([139], 4)
    """
    result = vals[:]
    num_vals = len(vals)
    for repeat in range(repeat_n):
        for val_pos in range(num_vals):
            idx =val_pos + repeat*num_vals
            next_value = result[idx]+1
            result.append(next_value if next_value < 10 else 1)
    return result

INFINITY = 100_000_000

def a_star(grid:Grid, start:Point, end:Point, h=lambda pt: pt.value):
    open_set:Set[Point] = {start}
    came_from:Dict[Point, Point] = {}
    g_score:Dict[Point, int] = {pt:INFINITY for pt in grid} # cheapest path to point from start
    g_score[start] = 0
    f_score:Dict[Point, int]  = {start: 0} # current best score to point
    while open_set:
        current = min(open_set, key=lambda pt: f_score[pt])
        if current == end:
            return reconstruct_path(came_from, current)
        open_set.remove(current)
        for neighbor in grid.around(current, include_diagonals=False):
            tentative_score = g_score[current] + neighbor.value #d(current, neighbor)
            if tentative_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_score
                f_score[neighbor] = tentative_score + h(neighbor)
                if neighbor not in open_set:
                    open_set.add(neighbor)
    raise KeyError('No path')

def reconstruct_path(came_from, current:Point):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def parse_txt(txt: str) -> Grid:
    lines = txt.strip().split('\n')
    rows :List[List[int]] = []
    for line in lines:
        row_data :List[int] = []
        for char in line:
            row_data.append(int(char))
        rows.append(row_data)
    print(rows)
    return Grid(rows)


def simulated_annealing(g: Grid, start:Point, end:Point) -> List[Point]:
    path = []
    for x in range(g.shape[0]):
        for y in range(g.shape[1]):
            path.append(g.get(x, y))
            if x < g.shape[0]-1:
                path.append(g.get(x+1, y))
    path_score = sum(p.value for p in path)


if __name__ == '__main__':
    #print(part1(SAMPLE))
    #print(part1(open('day15.txt').read())) #441
    # import doctest
    # doctest.testmod()
    # print(repeat_loop([1,3,9], 4))
    print(part2(SAMPLE)) # 315
    print(part2(open('day15.txt').read())) #441
