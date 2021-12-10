import collections

SAMPLE = '''3,4,3,1,2
'''

REAL_DATA = '''5,3,2,2,1,1,4,1,5,5,1,3,1,5,1,2,1,4,1,2,1,2,1,4,2,4,1,5,1,3,5,4,3,3,1,4,1,3,4,4,1,5,4,3,3,2,5,1,1,3,1,4,3,2,2,3,1,3,1,3,1,5,3,5,1,3,1,4,2,1,4,1,5,5,5,2,4,2,1,4,1,3,5,5,1,4,1,1,4,2,2,1,3,1,1,1,1,3,4,1,4,1,1,1,4,4,4,1,3,1,3,4,1,4,1,2,2,2,5,4,1,3,1,2,1,4,1,4,5,2,4,5,4,1,2,1,4,2,2,2,1,3,5,2,5,1,1,4,5,4,3,2,4,1,5,2,2,5,1,4,1,5,1,3,5,1,2,1,1,1,5,4,4,5,1,1,1,4,1,3,3,5,5,1,5,2,1,1,3,1,1,3,2,3,4,4,1,5,5,3,2,1,1,1,4,3,1,3,3,1,1,2,2,1,2,2,2,1,1,5,1,2,2,5,2,4,1,1,2,4,1,2,3,4,1,2,1,2,4,2,1,1,5,3,1,4,4,4,1,5,2,3,4,4,1,5,1,2,2,4,1,1,2,1,1,1,1,5,1,3,3,1,1,1,1,4,1,2,2,5,1,2,1,3,4,1,3,4,3,3,1,1,5,5,5,2,4,3,1,4
'''

def parse_text(txt):
    return [int(val) for val in txt.strip().split(',')]

def part_2(txt, days=80):
    """
    >>> sum(part_2(SAMPLE).values())
    5934
    >>> part_2(SAMPLE, days=1)
    >>> part_2(SAMPLE, days=2)
    """
    nums = parse_text(txt)
    day_counts = collections.Counter(nums)
    new_dict = {day:0 for day in range(9)}
    for day in range(days):
        for fish_age in range(1,8):
            new_dict[fish_age] = day_counts[fish_age+1]
        new_dict[0] = day_counts[1]
        new_dict[6] += day_counts[0]
        new_dict[8] = day_counts[0]
        day_counts = new_dict
        new_dict = {}
    return day_counts

def part_2_list(txt, days=80):
    """
    >>> sum(part_2_list(SAMPLE))
    5934
    >>> part_2_list(SAMPLE, days=1)
    >>> part_2_list(SAMPLE, days=2)
    """
    nums = parse_text(txt)
    day_counts = [0]*9  # index is the day number (holding num fish at that day)
    for day in nums:
        day_counts[day] += 1
    for day in range(days):
        day_counts = day_counts[1:] + day_counts[:1]
        day_counts[6] += day_counts[-1]
    return day_counts

def part_1(txt, days=80):
    """
    >>> part_1(SAMPLE)
    5934
    """
    nums = parse_text(txt)
    for day in range(days):
        nums = next_day(nums)
    return len(nums)


def next_day(nums):
    """
    >>> next_day([1,2,1,6,0,8])
    [0, 1, 0, 5, 6, 8, 7]
    """
    res = []
    for num in nums:
        if num == 0:
            res.append(6)
            res.append(8)
        else:
            res.append(num-1)
    return res


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print(part_1(REAL_DATA)) # 359999
    #print(part_1(REAL_DATA, days=256)) # 359999
    print(sum(part_2(SAMPLE).values())) # 5934
    print(sum(part_2(SAMPLE, days=256).values())) # 26_984_457_539


