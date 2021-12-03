SAMPLE = '''199
200
208
210
200
207
240
269
260
263
'''

def parse_txt(txt):
    """
    >>> parse_txt(SAMPLE)
    [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    """
    return [int(line) for line in txt.strip().split('\n')]

def part_1(nums):
    '''
    >>> part_1(parse_txt(SAMPLE))
    7
    '''
    return sum(num > prev for prev, num in zip(nums, nums[1:]))

def window(seq, size=3):
    # for i, item in enumerate(seq):
    #     yield seq[i:i+size]
    return (seq[i:i+size] for i, item in enumerate(seq))

def part_2(nums):
    return sum(sum(num) > sum(prev)
            for prev, num in zip(window(nums), window(nums[1:])))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print(part_1(parse_txt(open('day1.txt').read())))
    print(part_2(parse_txt(open('day1.txt').read())))

