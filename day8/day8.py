SMALL = '''acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
'''

SAMPLE = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

def parse_txt(txt):
    """
    >>> parse_txt(SMALL)
    [(['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'], ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf'])]
    """
    data = []
    for line in txt.strip().split('\n'):
        patterns, output = line.split(' | ')
        patterns = patterns.split()
        output = output.split()
        data.append((patterns, output))
    return data

def part_1(txt):
    """
    >>> part_1(SAMPLE)
    26
    """

    lines = parse_txt(txt)
    only1478 = 0
    for line in lines:
        patterns, outputs = line
        for output in outputs:
            if len(output) in {2,4,3,7}:
                only1478 += 1
    return only1478

def part_2(txt):
    """
    >>> part_2(SAMPLE)
    [8394, 9781, 1197, 9361, 4873, 8418, 4548, 1625, 8717, 4315]
    """
    lines = parse_txt(txt)
    values = []
    for line in lines:
        patterns, outputs = line
        mappings = get_mapping(patterns)
        val = []
        for output in outputs:
            val.append(mappings[''.join(sorted(output))])
        values.append(int(''.join(str(v) for v in val)))
    return values

def get_mapping(patterns):
    """
    Returns dict mapping string(segment) -> 0-9
    >>> get_mapping(parse_txt(SMALL)[0][0])
    {'abcdefg': 8, 'abd': 7, 'abef': 4, 'ab': 1, 'bcdef': 5, 'acdfg': 2, 'abcdf': 3, 'abcdef': 9, 'bcdefg': 6, 'abcdeg': 0}
    """
    #breakpoint()
    patterns = list(''.join(sorted(p)) for p in patterns)
    result = {} # segments (sorted string) -> digit
    inverse_result = {} # digit -> set segments
    # find easy digits
    len2digit = {2:1, 4:4, 3:7, 7:8}

    for pattern in patterns:
        if digit := len2digit.get(len(pattern), None):
            result[pattern] = digit
            inverse_result[digit] = set(pattern)
    for pattern in patterns:
        chars = set(pattern)
        if len(pattern) == 6:
            if inverse_result[4] <= chars:
                val = 9
            elif inverse_result[1] <= chars:
                val = 0
            else:
                val = 6
            result[pattern] = val
            inverse_result[val] = chars
        elif len(pattern) == 5:
            if inverse_result[1] <= chars:
                val = 3
            elif (inverse_result[4] - inverse_result[1]) <= chars:
                val = 5
            else:
                val = 2
            result[pattern] = val
            inverse_result[val] = chars
    return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(part_1(SAMPLE)) #26
    print(part_1(open('day8.txt').read())) #367
    print(sum(part_2(open('day8.txt').read()))) #974512

    #print(get_mapping(parse_txt(SMALL)[0][0]))
