def find_increase_count(txt):
    r'''
    >>> find_increase_count('199\n200\n208\n210\n200')
    3

    Can convert this to a comprehension by summing list instead of incrementing
    '''
    nums = []
    for line in txt.strip().split('\n'):
        nums.append(int(line.strip()))
    increase = 0
    prev = None
    #prev, *nums = nums
    for num in nums:
        if prev:
            if num > prev:
                increase += 1
        prev = num
    return increase


def runner(fname):
    print(find_increase_count(open(fname).read()))

def window_iter_bad(seq, size=3):
    it = iter(seq)
    window = []
    while item:=next(it):
        window.append(item)
        if len(window) >= size:
            yield window[-size:]

def window_iter(seq, size=3):
    window = []
    for item in seq:
        window.append(item)
        if len(window) >= size:
            yield window[-size:]

def find_increase_window(txt, window_size=3):
    r'''
    >>> find_increase_window('199\n200\n208\n210\n200\n207\n240\n269\n260\n263\n')
    5
    '''
    nums = [int(line.strip()) for line in txt.strip().split('\n')]
    prev = None
    increase = 0
    for window in window_iter(nums):
        if prev and sum(window) > sum(prev):
            increase += 1
        prev = window
    return increase

def runner2(fname):
    print(find_increase_window(open(fname).read()))


def one_liner(fname):
    txt = open(fname).read()
    nums = [int(line.strip()) for line in txt.strip().split('\n')]
    print(sum(b>a for a,b in zip(nums, nums[1:])))

def one_liner_expanded(fname):
    txt = open(fname).read()
    nums = [int(line.strip()) for line in txt.strip().split('\n')]
    vals = []
    for a, b in zip(nums, nums[1:]):
        vals.append(b > a)
    print(sum(vals))


def one_liner_part2(fname):
    txt = open(fname).read()
    nums = [int(line.strip()) for line in txt.strip().split('\n')]
    print(sum(b>a for a,b in zip(nums, nums[3:])))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    runner('day1.txt')
    runner2('day1.txt')
    one_liner_expanded('day1.txt')
    one_liner_part2('day1.txt')
    
