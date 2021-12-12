import sys
sys.path.append('../gridder/')
from grid import Grid

SAMPLE = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''

def parse_data(lines, grid_class=Grid):
    r"""
    >>> parse_data(SAMPLE.strip().split('\n'))
    ([7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1], [[[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]], [[3, 15, 0, 2, 22], [9, 18, 13, 17, 5], [19, 8, 7, 25, 23], [20, 11, 10, 24, 4], [14, 21, 16, 12, 6]], [[14, 21, 17, 24, 4], [10, 16, 15, 9, 19], [18, 8, 23, 26, 20], [22, 11, 13, 6, 5], [2, 0, 12, 3, 7]]])
    """
    nums = [int(val) for val in lines[0].split(',')]
    boards = [[[int(val) for val in line.strip().split()] for line in lines[i:i+5]]
              for i in range(2, len(lines), 6)]
    grids = [grid_class(b, pt_class=BingoPoint)for b in boards]
    return nums, grids

from dataclasses import dataclass, field
@dataclass(unsafe_hash=True)
class BingoPoint:
    x: int
    y: int
    value: object = field(hash=False)
    found: object = field(default=False, hash=False)


def solved(grid):
    for row in grid.rows:
        if all(pt.found for pt in row):
            return True
    for col in grid.columns():
        if all(pt.found for pt in col):
            return True
    return False

def part1(txt):
    nums, grids = parse_data(txt)
    done = False
    for num in nums:
        for g in grids:
            for pt in g:
                if pt.value == num:
                    pt.found = True
            if solved(g):
                done = True
                break
        if done:
            break
    sum_unmarked = sum(pt.value for pt in g if not pt.found)
    return num * sum_unmarked

class BingoBoard(Grid):
    def solve(self, nums):
        for round, num in enumerate(nums):
            for pt in self:
                if pt.value == num:
                    pt.found = True
            if self.solved():
                done = True
                break
        self.finish_round = round
        self.finish_num = num

    def solved(self):
        for row in self.rows:
            if all(pt.found for pt in row):
                return True
        for col in self.columns():
            if all(pt.found for pt in col):
                return True
        return False

    def sum_unmarked(self):
        return sum(pt.value for pt in self if not pt.found)

def part2(txt):
    nums, boards = parse_data(txt, grid_class=BingoBoard)
    [b.solve(nums) for b in boards]
    winner = max(boards, key=lambda board:board.finish_num)
    print(f'{winner.finish_num * winner.sum_unmarked()}')




if __name__ == '__main__':
    print(part1(SAMPLE.split('\n'))) # 4512
    print(part1(open('day4.txt').read().split('\n'))) # 29440
    part2(SAMPLE.split('\n'))
    part2(open('day4.txt').read().split('\n'))

