#from collections import namedtuple
from dataclasses import dataclass, field
from typing import List

#Point = namedtuple('Point', 'x,y,value')

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
        self.rows = []
        for y, row in enumerate(data):
            this_row = []
            for x, val in enumerate(row):
                this_row.append(pt_class(x,y,val))
            self.rows.append(this_row)
        self.shape = (len(data[0]), len(data))

    def __iter__(self): 
        for row in self.rows:
            yield from row


    def columns(self):
        for x in range(self.shape[0]):
            yield [self.rows[y][x] for y in range(self.shape[1])]

    def __str__(self):
        lines = []
        for row in self.rows:
            line = ' '.join([f'{pt.value:3}' for pt in row])
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

