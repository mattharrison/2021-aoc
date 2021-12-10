SAMPLE = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
'''

def parse_txt(txt):
    return txt.strip().split('\n')

def part1(txt):
    """
    >>> part1(SAMPLE)
    26397
    """
    lines = parse_txt(txt)
    scores = dict(zip(')]}>', [3, 57, 1197, 25_137]))
    score = 0
    for line in lines:
        results = find_illegal_move(line)
        if results[0]:
            expected, got, remaining = results
            score += scores[got]
    return score

def part2(txt):
    """
    >>> part2(SAMPLE)
    288957
    """
    lines = parse_txt(txt)
    scores = dict(zip(')]}>', [1, 2, 3, 4]))
    all_scores = []
    for line in lines:
        score = 0
        expected, got, remaining = find_illegal_move(line)
        if got:
            continue
        for char in remaining:
            score *=5
            score += scores.get(char, 0)
        #print(remaining, score)
        all_scores.append(score)
    
    return sorted(all_scores)[(len(all_scores)-1)//2]


def find_illegal_move(line):
    """
    Return expected, got, remaining
    None if good
    >>> find_illegal_move('[)')
    (']', ')', ']')
    """
    expected = []
    mapping = dict(zip('[<({', ']>)}'))
    for char in line:
        if next_char := mapping.get(char):
            expected.append(next_char)
        elif char != expected[-1]:
            return expected[-1], char, ''.join(expected)[::-1]
        else:
            expected.pop()
    return None, None, ''.join(expected)[::-1]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print(part1(open('day10.txt').read())) # 339411
    print(part2(open('day10.txt').read())) # 2289754624
