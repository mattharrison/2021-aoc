
SAMPLE = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'''

def parse_txt(txt):
    """
    >>> parse_txt(SAMPLE)

    """
    pts, folds = txt.strip().split('\n\n')
    coords = []

    for line in pts.split('\n'):
        x,y = line.split(',')
        coords.append((int(x), int(y)))
    #coords = [(int(x), int(y)) for line in pts.split('\n') for x,y in line.split(',')]
    return coords, folds.split('\n')


def part2(txt):
    coords, folds = parse_txt(txt)
    grid = {}
    for x,y in coords:
        grid[(x,y)] = 1
    for fold in folds:
        max_x = max(grid, key=lambda tup: tup[0])[0]
        max_y = max(grid, key=lambda tup: tup[1])[1]

        axis, amount = fold.split()[-1].split('=')
        amount = int(amount)
        new_grid = {}
        for coord in grid:
            x,y = coord
            if axis == 'x':
                if x > amount:
                    new_x = amount - (x - amount)
                    new_grid[(new_x, y)] = 1
                else:
                    new_grid[(x, y)] = 1
            if axis == 'y':
                if y > amount:
                    new_y = amount - (y - amount)
                    new_grid[(x, new_y)] = 1
                else:
                    new_grid[(x, y)] = 1
        grid = new_grid
    return new_grid

def print_grid(grid):
    max_x = max(grid, key=lambda tup: tup[0])[0]
    max_y = max(grid, key=lambda tup: tup[1])[1]
    matrix = [['.' for x in range(max_x+1)] for y in range(max_y+1)]
    print(max_x, max_y)
    print(len(matrix[0]), len(matrix))
    for x,y in grid:
        try:
            matrix[y][x] = '#'
        except IndexError:
            print(x,y)
            raise
    print('\n'.join(''.join(line) for line in matrix))

def part1(txt):
    """
    >>> part1(SAMPLE)
    """

    coords, folds = parse_txt(txt)
    folds = folds[:1]
    grid = {}
    for x,y in coords:
        grid[(x,y)] = 1
    max_x = max(grid, key=lambda tup: tup[0])[0]
    max_y = max(grid, key=lambda tup: tup[1])[1]
    for fold in folds:
        axis, amount = fold.split()[-1].split('=')
        amount = int(amount)
        new_grid = {}
        for coord in grid:
            x,y = coord
            if axis == 'x':
                if x > amount:
                    new_x = amount - (x - amount)
                    new_grid[(new_x, y)] = 1
                else:
                    new_grid[(x, y)] = 1
            if axis == 'y':
                if y > amount:
                    new_y = amount - (y - amount)
                    new_grid[(x, new_y)] = 1
                else:
                    new_grid[(x, y)] = 1
    return new_grid

if __name__ == '__main__':
    import doctest
    #doctest.testmod()
    #breakpoint()
    print(len(part1(SAMPLE)))
    print(len(part1(open('day13.txt').read()))) # 735
    print(print_grid(part2(open('day13.txt').read()))) # CAFJHZCK
