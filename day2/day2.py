SAMPLE = '''forward 5
down 5
forward 8
up 3
down 8
forward 2
'''

def parse_data(txt):
    """
    >>> list(parse_data(SAMPLE))
    [('forward', 5), ('down', 5), ('forward', 8), ('up', 3), ('down', 8), ('forward', 2)]
    """
    for line in txt.strip().split('\n'):
        direction, amount = line.split()
        amount = int(amount)
        yield direction, amount

def get_position(directions):
    x, y = 0, 0
    for direction, amount in directions:
        if direction == 'forward':
            x += amount
        elif direction == 'down':
            y += amount
        elif direction == 'up':
            y -= amount
    return x, y

def part1(txt):
    directions = parse_data(txt)
    x, y = get_position(directions)
    print(f'{x=} {y=} {x*y=}')


def get_aim_position(directions):
    x, y, aim = 0, 0, 0
    for direction, amount in directions:
        if direction == 'forward':
            x += amount
            y += aim*amount
        elif direction == 'down':
            aim += amount
        elif direction == 'up':
            aim -= amount
    return x, y

def part2(txt):
    directions = parse_data(txt)
    x, y = get_aim_position(directions)
    print(f'{x=} {y=} {x*y=}')



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    part1(SAMPLE)
    part1(open('day2.txt').read())
    part2(SAMPLE)
    part2(open('day2.txt').read())
