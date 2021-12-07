import collections

SAMPLE = '''3,4,3,1,2
'''

REAL_DATA = '''5,3,2,2,1,1,4,1,5,5,1,3,1,5,1,2,1,4,1,2,1,2,1,4,2,4,1,5,1,3,5,4,3,3,1,4,1,3,4,4,1,5,4,3,3,2,5,1,1,3,1,4,3,2,2,3,1,3,1,3,1,5,3,5,1,3,1,4,2,1,4,1,5,5,5,2,4,2,1,4,1,3,5,5,1,4,1,1,4,2,2,1,3,1,1,1,1,3,4,1,4,1,1,1,4,4,4,1,3,1,3,4,1,4,1,2,2,2,5,4,1,3,1,2,1,4,1,4,5,2,4,5,4,1,2,1,4,2,2,2,1,3,5,2,5,1,1,4,5,4,3,2,4,1,5,2,2,5,1,4,1,5,1,3,5,1,2,1,1,1,5,4,4,5,1,1,1,4,1,3,3,5,5,1,5,2,1,1,3,1,1,3,2,3,4,4,1,5,5,3,2,1,1,1,4,3,1,3,3,1,1,2,2,1,2,2,2,1,1,5,1,2,2,5,2,4,1,1,2,4,1,2,3,4,1,2,1,2,4,2,1,1,5,3,1,4,4,4,1,5,2,3,4,4,1,5,1,2,2,4,1,1,2,1,1,1,1,5,1,3,3,1,1,1,1,4,1,2,2,5,1,2,1,3,4,1,3,4,3,3,1,1,5,5,5,2,4,3,1,4
'''

def parse_txt(txt):
    return [int(x) for x in txt.strip().split(',')]

def next_day(vals):
    """
    >>> next_day([3,4,3,1,2])
    [2, 3, 2, 0, 1]
    """
    res = []
    for num in vals:
        if num == 0:
            res.append(8)
            res.append(6)
        else:
            res.append(num - 1)
    return res

def part1(txt, days=80):
    """
    >>> part1(SAMPLE)
    5934
    """
    nums = parse_txt(txt)
    for day in range(days):
        nums = next_day(nums)
    print(len(nums))

def part2(txt, days=80):
    """
    SAMPLE = 3,4,3,1,2

    >>> part2(SAMPLE, days=1)
    {0: 1, 1: 1, 2: 2, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    >>> part2(SAMPLE, days=2)
    {1: 2, 2: 1, 3: 0, 4: 0, 5: 0, 6: 1, 7: 0, 0: 1, 8: 1}

    """
    nums = parse_txt(txt)
    day_counts = collections.Counter(nums)
    for i in range(9):
        day_counts.setdefault(i, 0)
    new_dict = {i:0 for i in range(9)}    
    for day in range(days):
        for fish_age in [1,2,3,4,5,6,7]:
            new_dict[fish_age] = day_counts[fish_age+1]
        new_dict[0] = day_counts[1]
        new_dict[8] = day_counts[0]
        new_dict[6] += day_counts[0]
        day_counts = new_dict
        new_dict = {}
    return day_counts


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    part1(SAMPLE)  # 5934
    part1(REAL_DATA)  # 359999
    #part1(SAMPLE, days=256)
    print(sum(part2(SAMPLE).values()))
    print(sum(part2(REAL_DATA, days=256).values())) #1631647919273
