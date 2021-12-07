import collections

SAMPLE = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
'''


def parse_txt(txt):
    """
    >>> parse_txt(SAMPLE)
    [((0, 9), (5, 9)), ((8, 0), (0, 8)), ((9, 4), (3, 4)), ((2, 2), (2, 1)), ((7, 0), (7, 4)), ((6, 4), (2, 0)), ((0, 9), (2, 9)), ((3, 4), (1, 4)), ((0, 0), (8, 8)), ((5, 5), (8, 2))]
    """
    # probably easier for regex here
    coords = []
    for line in txt.strip().split('\n'):
        src, dst = line.split(' -> ')
        x_src, y_src = tuple(int(val) for val in src.split(','))
        x_dst, y_dst = tuple(int(val) for val in dst.split(','))

        coords.append(((x_src, y_src), (x_dst, y_dst)))
    #coords = [tuple(int(pt) for pt in line.strip(' -> ')) for line in txt.strip().split('\n')]
    return coords

def is_flat(src, dst):
    """
    >>> is_flat( (2,2), (2,1))
    True
    >>> is_flat( (6,4), (2,0))
    False
    """
    return src[0] == dst[0] or src[1] == dst[1]

def enum_pts_in_line(src, dst):
    """
    >>> list(enum_pts_in_line((1,1), (1,3)))
    [(1, 1), (1, 2), (1, 3)]
    >>> list(enum_pts_in_line((1,1), (3,3)))
    [(1, 1), (2, 2), (3, 3)]
    """
    if is_flat(src, dst):
        min_x = min(src[0], dst[0])
        max_x = max(src[0], dst[0])
        min_y = min(src[1], dst[1])
        max_y = max(src[1], dst[1])
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                yield (x,y)
    else:
        for x, y in zip(enum_pts(src[0], dst[0]), enum_pts(src[1], dst[1])):
            yield (x, y)

def enum_pts(start, end):
    """
    >>> list(enum_pts(0, 7))
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> list(enum_pts(10, 7))
    [10, 9, 8, 7]
    """
    if start > end:
        yield from range(start, end-1, -1)
    else:
        yield from range(start, end+1)


def part1(txt):
    """
    >>> part1(SAMPLE)
    5
    """
    coords = parse_txt(txt)
    counter = collections.Counter()
    for src, dst in coords:
        if is_flat(src, dst):
            for xy in enum_pts_in_line(src, dst):
                counter[xy] += 1
        #print(f'{src=} {dst=} {counter=}')
    print(len([v for v in counter.values() if v > 1]))


def part2(txt):
    """
    >>> part2(SAMPLE)
    12
    """
    coords = parse_txt(txt)
    counter = collections.Counter()
    for src, dst in coords:

        for xy in enum_pts_in_line(src, dst):
            counter[xy] += 1
        #print(f'{src=} {dst=} {counter=}')
    print(len([v for v in counter.values() if v > 1]))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    part1(open('day5.txt').read())
    part2(open('day5.txt').read())
