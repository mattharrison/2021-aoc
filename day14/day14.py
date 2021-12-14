from collections import Counter

SAMPLE = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
'''

def parse_txt(txt):
    """
    >>> parse_txt(SAMPLE)
    ('NNCB', {'CH': 'B', 'HH': 'N', 'CB': 'H', 'NH': 'C', 'HB': 'C', 'HC': 'B', 'HN': 'C', 'NN': 'C', 'BH': 'H', 'NC': 'B', 'NB': 'B', 'BN': 'B', 'BB': 'N', 'BC': 'B', 'CC': 'N', 'CN': 'C'})
    """
    template, rules = txt.strip().split('\n\n')
    insertion_rules = {}
    for line in rules.split('\n'):
        neighbors, insert = line.split(' -> ')
        insertion_rules[neighbors] = insert
    return template, insertion_rules


def part1(txt, steps=5):
    """
    >>> part1(SAMPLE, steps=1)
    (Counter({'N': 2, 'C': 2, 'B': 2, 'H': 1}), Counter({'NC': 1, 'CN': 1, 'NB': 1, 'BC': 1, 'CH': 1, 'HB': 1, 'NN': 0, 'CB': 0}))
    >>> pairs = part1(SAMPLE, steps=10)
    >>> pairs
    """
    template, insertion_rules = parse_txt(txt)
    pairs = Counter(''.join(pair) for pair in zip(template, template[1:])) # pairs to count
    letter_counts = Counter(template)
    for step in range(steps):
        new_count = Counter(pairs)
        for pair in list(pairs.keys()):
            left, right = pair
            to_insert = insertion_rules[pair]
            new_count[pair] -= pairs[pair]
            new_count[left+to_insert] += pairs[pair]
            new_count[to_insert+right] += pairs[pair]
            letter_counts[to_insert] += pairs[pair]
        pairs = new_count
    print(max(letter_counts.values()) - min(letter_counts.values()))
    return pairs, letter_counts

        
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    part1(SAMPLE, 10) #1588
    part1(open('day14.txt').read(), 10) #3306
    part1(SAMPLE, 40) #2188189693529
    part1(open('day14.txt').read(), 40) #3760312702877

