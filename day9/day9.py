from collections import namedtuple
import functools

SAMPLE = '''2199943210
3987894921
9856789892
8767896789
9899965678
'''


def parse_txt(txt):
    """
    >>> parse_txt(SAMPLE)
    [[2, 1, 9, 9, 9, 4, 3, 2, 1, 0], [3, 9, 8, 7, 8, 9, 4, 9, 2, 1], [9, 8, 5, 6, 7, 8, 9, 8, 9, 2], [8, 7, 6, 7, 8, 9, 6, 7, 8, 9], [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]]
    """
    return [[int(v) for v in line] for line in txt.strip().split('\n')]

Position = namedtuple('Position', 'x,y,value')

class HeightMap:
    def __init__(self, vals):
        self.vals = vals
        self.shape = (len(vals[0]), len(vals))

    def __iter__(self):
        # return (x,y), val
        for y, row in enumerate(self.vals):
            for x, val in enumerate(row):
                yield Position(x,y, val)

    def __str__(self):
        res = []
        for pos in self:
            res.append(pos)
        return ''.join(res)

    def points_around(self, pos):
        x, y, value = pos
        for delta_x, delta_y in [(-1,0), (1,0), (0,-1), (0,1)]:
            x1 = x + delta_x
            y1 = y + delta_y
            if 0 <= x1 < self.shape[0] and 0 <= y1 < self.shape[1]:
                 yield Position(x1, y1, self.vals[y1][x1])

    def low_points(self):
        minimums = []
        for pos in self:
            x,y, val = pos
            if all(val<val2 for x2,y2, val2 in self.points_around(pos)):
                minimums.append(Position(x,y,val))
        return minimums

    def basins(self):
        minimums = self.low_points()
        basins = []
        for pos in minimums:
            basins.append(self.get_basin(pos))
        return basins

    def get_basin(self, start_pos):
        """
        >>> map = HeightMap(SAMPLE)

        """
        seen = set() # pos
        to_visit = [start_pos]
        while to_visit:
            pos = to_visit.pop()
            seen.add(pos)
            for other_pos in self.points_around(pos):
                x,y,val = other_pos
                if val == 9:
                    continue
                elif val > pos.value:
                    to_visit.append(other_pos)
        return seen

def part2(txt):
    map = HeightMap(parse_txt(txt))
    basins = map.basins()
    lengths = [len(b) for b in basins]
    lengths.sort()
    print(lengths)
    return functools.reduce(lambda x,y: x*y, lengths[-3:])

def part1(txt):
    """
    >>> part1(SAMPLE)
    15
    """
    map = HeightMap(parse_txt(txt))
    minimums = map.low_points()
    return sum(1+m.value for m in minimums)




if __name__ == '__main__':
    import doctest
    #doctest.testmod()
    print(part1(SAMPLE)) # 15
    print(part1(open('day9.txt').read())) # 514
    map = HeightMap(parse_txt(SAMPLE))
    #breakpoint()
    print(len(map.get_basin(map.low_points()[3])))
    print(part2(SAMPLE)) # 1134
    print(part2(open('day9.txt').read())) # 1103130

