from collections import Counter

SAMPLE = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''

def part1_as_string(txt):
    """
    >>> part1_as_string(SAMPLE)
    """
    counter = Counter()
    for line in txt.strip().split('\n'):
        for i, val in enumerate(line):
            counter[(i,val)] += 1
    gamma = []
    for i in range(len(line)):
        gamma.append(max(['0','1'], key=lambda val, i=i, counter=counter: counter[(i,val)]))
    gamma = int(''.join(gamma), 2)
    epsilon = gamma ^ int('1'*len(line), 2)
    return gamma * epsilon


def part2_as_string(txt):
    """
    >>> part2_as_string(SAMPLE)
    23, 10
    """
    lines = txt.strip().split('\n')
    o2_lines = lines[:]
    bit_pos = 0
    while len(o2_lines) > 1:
        count_1s = sum(line[bit_pos] == '1' for line in o2_lines)
        if count_1s >= len(o2_lines)/2:
            o2_lines = [line for line in o2_lines if line[bit_pos] == '1']
        else:
            o2_lines = [line for line in o2_lines if line[bit_pos] == '0']

        bit_pos += 1
    bit_pos = 0
    co2_lines = lines[:]
    while len(co2_lines) > 1:
        count_1s = sum(line[bit_pos] == '1' for line in co2_lines)
        least_common = '0' if count_1s >= len(co2_lines)/2 else '1'
        co2_lines = [line for line in co2_lines if line[bit_pos] == least_common]
        #print(f'{co2_lines=}, {bit_pos=}, {count_1s=}, {least_common=}')
        bit_pos += 1

    o2_rating = int(o2_lines[0], 2)
    co2_rating = int(co2_lines[0], 2)
    return o2_rating, co2_rating, o2_rating*co2_rating

if __name__ == '__main__':
    #breakpoint()
    print(part1_as_string(SAMPLE))
    print(part1_as_string(open('day3.txt').read()))
    print(part2_as_string(SAMPLE))
    print(part2_as_string(open('day3.txt').read()))
