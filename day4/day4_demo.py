
SAMPLE ='''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

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

def parse_lines(txt):
    """
    >>> parse_lines(SAMPLE)
    ([7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1], [[[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]], [[3, 15, 0, 2, 22], [9, 18, 13, 17, 5], [19, 8, 7, 25, 23], [20, 11, 10, 24, 4], [14, 21, 16, 12, 6]], [[14, 21, 17, 24, 4], [10, 16, 15, 9, 19], [18, 8, 23, 26, 20], [22, 11, 13, 6, 5], [2, 0, 12, 3, 7]]])
    """
    lines = txt.strip().split('\n')
    nums = [int(val) for val in lines[0].split(',')]
    boards = []
    for i in range(1, len(lines), 6):
        board = []
        lines_in_board = lines[i:i+6]
        for line in lines_in_board:
            if not line:
                continue
            board.append([int(val) for val in line.split()])
        boards.append(board)
    return nums, boards

def invert_board(board):
    """
    >>> invert_board([[14, 21, 17, 24, 4], [10, 16, 15, 9, 19], [18, 8, 23, 26, 20], [22, 11, 13, 6, 5], [2, 0, 12, 3, 7]])
    {14: (0, 0), 21: (1, 0), 17: (2, 0), 24: (3, 0), 4: (4, 0), 10: (0, 1), 16: (1, 1), 15: (2, 1), 9: (3, 1), 19: (4, 1), 18: (0, 2), 8: (1, 2), 23: (2, 2), 26: (3, 2), 20: (4, 2), 22: (0, 3), 11: (1, 3), 13: (2, 3), 6: (3, 3), 5: (4, 3), 2: (0, 4), 0: (1, 4), 12: (2, 4), 3: (3, 4), 7: (4, 4)}

    """
    return {val:(x,y) for y, row in enumerate(board) for x, val in enumerate(row)}
    # for y, row in enumerate(board):
    #     for x, val in enumerate(row):
    #         inverted[val] = (x,y)
    # return inverted

def part_1oo(txt):
    """
    >>> part_1oo(SAMPLE)
    4512
    """
    nums, boards_data = parse_lines(txt)
    boards = [Board(data) for data in boards_data]
    for b in boards:
        b.solve(nums)
    winner = min(boards, key=lambda b:b.finish_round)
    return winner.num_to_finish * sum(winner.get_unmarked())

def part_2oo(txt):
    """
    >>> part_2oo(SAMPLE)
    1924
    """
    nums, boards_data = parse_lines(txt)
    boards = [Board(data) for data in boards_data]
    for b in boards:
        b.solve(nums)
    winner = max(boards, key=lambda b:b.finish_round)
    return winner.num_to_finish * sum(winner.get_unmarked())

def part_1(txt):
    """
    >>> part_1(SAMPLE)
    4512
    """
    nums, boards = parse_lines(txt)
    #inverted_boards = [invert_board(b) for b in boards]
    inverted_boards = []
    for b in boards:
        inverted_boards.append(invert_board(b))
    seen_boards = [set() for b in boards]  # (x,y) of found spots for each board
    for num in nums:
        done = False
        for i, board in enumerate(boards):
            inverted_board = inverted_boards[i]
            seen_board = seen_boards[i]
            loc = inverted_board[num]
            seen_board.add(loc)
            if solved(board, seen_board):
                done = True
                break
        if done:
            break
    unmarked = get_unmarked(board, seen_board)
    return num*sum(unmarked)

class Board:
    def __init__(self, data):
        self.data = data # list of lists
        self.inverted = invert_board(data)
        self.seen = set() 
        self.finish_round = None
        self.num_to_finish = None

    def solve(self, nums):
        for round, num in enumerate(nums):
            #if num in self.inverted:
            #    loc = self.inverted[num]
            if loc := self.inverted.get(num, None):
                self.seen.add(loc)
            if self.check():
                self.finish_round = round
                self.num_to_finish = num
                break

    def check(self):
        return solved(self.data, self.seen)
    def get_unmarked(self):
        return get_unmarked(self.data, self.seen)

def get_unmarked(board, seen_board):
    return [val for y, row in enumerate(board) for x, val in enumerate(row) if (x,y) not in seen_board]
    # for y, row in enumerate(board):
    #     for x, val in enumerate(row):
    #         if (x,y) not in seen_board:
    #             unmarked.append(val)
    # return unmarked

def solved(board, seen_board):
    """
    >>> solved([[1,2], [3,4]], {(0,0), (0,1)})
    True
    >>> solved([[1,2], [3,4]], {(0,0), (1,1)})
    False
    """
    size = len(board)
    for y in range(size):  # rows
        if all((x,y) in seen_board for x in range(size)):
            return True
    for x in range(size):  # colums
        if all((x,y) in seen_board for y in range(size)):
            return True
    return False




if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #breakpoint()
    #parse_lines(SAMPLE)
