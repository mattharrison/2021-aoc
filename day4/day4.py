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

def parse_data(lines):
    r"""
    >>> parse_data(SAMPLE.strip().split('\n'))
    ([7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1], [[[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]], [[3, 15, 0, 2, 22], [9, 18, 13, 17, 5], [19, 8, 7, 25, 23], [20, 11, 10, 24, 4], [14, 21, 16, 12, 6]], [[14, 21, 17, 24, 4], [10, 16, 15, 9, 19], [18, 8, 23, 26, 20], [22, 11, 13, 6, 5], [2, 0, 12, 3, 7]]])
    """
    nums = [int(val) for val in lines[0].split(',')]
    #boards = [lines[i:i+5] for i in range(2, len(lines), 6)]
    # boards = []
    # for i in range(2, len(lines), 6):
    #     board_lines = lines[i:i+5]
    #     board = [[int(val) for val in line.strip().split()] for line in board_lines]
    #     boards.append(board)
    boards = [[[int(val) for val in line.strip().split()] for line in lines[i:i+5]]
              for i in range(2, len(lines), 6)]
    return nums, boards

def invert_board(board):
    """
    >>> b = [[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]]
    >>> invert_board(b)
    {22: (0, 0), 13: (1, 0), 17: (2, 0), 11: (3, 0), 0: (4, 0), 8: (0, 1), 2: (1, 1), 23: (2, 1), 4: (3, 1), 24: (4, 1), 21: (0, 2), 9: (1, 2), 14: (2, 2), 16: (3, 2), 7: (4, 2), 6: (0, 3), 10: (1, 3), 3: (2, 3), 18: (3, 3), 5: (4, 3), 1: (0, 4), 12: (1, 4), 20: (2, 4), 15: (3, 4), 19: (4, 4)}
    """
    inverted = {}
    for y, row in enumerate(board):
        for x, val in enumerate(row):
            inverted[val] = (x,y)
    return inverted

def solved(board, found_board):
    """
    >>> solved([[1,2], [3,4]], {(0,0), (0,1)})
    True
    >>> solved([[1,2], [3,4]], {(0,0), (1,1)})
    True
    >>> solved([[1,2], [3,4]], {(0,0)})
    False
    """
    size = len(board)
    # check rows
    for y in range(size):
        if all((x,y) in found_board for x in range(size)):
            return True
    # check cols
    for x in range(size):
        if all((x,y) in found_board for y in range(size)):
            return True
    # diags
    if all((i,i) in found_board for i in range(size)):
        return True
    if all((i,i) in found_board for i in range(size, -1, -1)):
        return True
    return False



def get_sum_unmarked(board, found_board):
    """
    >>> get_sum_unmarked([[1,2], [3,4]], {(0,0), (0,1)})
    6
    """
    unmarked = []
    for y, row in enumerate(board):
        for x, val in enumerate(row):
            if (x,y) not in found_board:
                unmarked.append(val)
    return sum(unmarked)

def part_1(nums, boards):
    r"""
    >>> nums, boards = parse_data(SAMPLE.split('\n'))
    >>> nums
    [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1]
    >>> part_1(nums, boards)
    """
    found_boards = [set() for b in boards] #(x,y) of found spots for each board
    inverted_boards = [invert_board(b) for b in boards]
    #print(nums)
    done = False
    while not (done):
        num, *nums = nums
        #print(f'{num=}, {nums=}')
        for i, board in enumerate(boards):
            if loc := inverted_boards[i].get(num):
                found_boards[i].add(loc)
            if solved(board, found_boards[i]):
                done = True
                break
    val = get_sum_unmarked(board, found_boards[i])
    print(f'{board=} {found_boards[i]=}, {val=} {num=} {num*val=}')

def max_index(seq):
    max_val = seq[0]
    max_i = None
    for i, val in enumerate(seq):
        if val >= max_val:
            max_i = i
    return max_i

def part_2(nums, boards):
    found_boards = [set() for b in boards] #(x,y) of found spots for each board
    inverted_boards = [invert_board(b) for b in boards]
    board_finish_round = [0 for b in boards]
    board_finish_val = [0 for b in boards]
    finished = set()
    for round, num in enumerate(nums):
        for i, board in enumerate(boards):
            if i in finished:
                continue
            if loc := inverted_boards[i].get(num):
                found_boards[i].add(loc)
            if solved(board, found_boards[i]):
                board_finish_round[i] = round
                board_finish_val[i] = num
                finished.add(i)
            if len(finished) == len(boards):
                break
    print(board_finish_round)
    board_index = max_index(board_finish_round)
    val = get_sum_unmarked(boards[board_index], found_boards[board_index])
    finish_num = board_finish_val[board_index]
    print(f'Part 2 {board_index=} {found_boards[board_index]=}, {finish_num*val=}')


def part2_oo(nums, boards_data):
    boards = [Board(data) for data in boards_data]
    [b.solve(nums) for b in boards]
    winner = max(boards, key=lambda board:board.finish_round)
    print(f'{winner.num_to_finish * get_sum_unmarked(winner.data, winner.found)}')


def part1_oo(nums, boards_data):
    boards = [Board(data) for data in boards_data]
    [b.solve(nums) for b in boards]
    winner = min(boards, key=lambda board:board.finish_round)
    print(f'{winner.num_to_finish * get_sum_unmarked(winner.data, winner.found)}')

class Board:
    def __init__(self, data):
        self.data = data # list of list
        self.inverted = invert_board(self.data) # mapping of num -> (x,y)
        self.found = set() # (x,y) spot for board
        self.finish_round = None
        self.num_to_finish = None

    def solve(self, nums):
        for round, num in enumerate(nums):
            if loc := self.inverted.get(num):
                self.found.add(loc)
            if self.check():
                self.finish_round = round
                self.num_to_finish = num
                break

    def check(self):
        size = len(self.data)
        # check rows
        for y in range(size):
            if all((x,y) in self.found for x in range(size)):
                return True
        # check cols
        for x in range(size):
            if all((x,y) in self.found for y in range(size)):
                return True
        # diags
        if all((i,i) in self.found for i in range(size)):
            return True
        if all((i,i) in self.found for i in range(size, -1, -1)):
            return True
        return False
    
            
        

if __name__ == '__main__':
    import doctest
    #doctest.testmod()
    #breakpoint()
    nums, boards = parse_data(SAMPLE.split('\n'))
    #part_1(nums, boards)   # 4512
    #part_2(nums, boards)   # 1924
    part1_oo(nums, boards)   # 4512
    part2_oo(nums, boards)   # 1924
    nums, boards = parse_data(open('day4.txt').read().split('\n'))
    part_1(nums, boards)   # 29440
    part1_oo(nums, boards)   # 29440
    part2_oo(nums, boards)   # 13884
    #part_2(nums, boards) # 22572


    

