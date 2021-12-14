from collections import Counter
from typing import List

class NodeRegistry:
    def __init__(self):
        self.value2node = {}

    def get(self, value):
        return self.value2node.setdefault(value, Node(value))

    def add(self, value, node):
        self.value2node[value] = node

    def __contains__(self, value):
        return value in self.value2node


class Node:
    def __init__(self, value):
        self.value = value
        self.others = []
        self.color = None

    def __repr__(self):
        return f'N({self.value})'

    def __hash__(self):
        return hash(self.value)

WHITE = 1
NIL = 2
GREY = 3
BLACK = 4

class Graph:
    def __init__(self):
        self.nodes:List[Node] = []

    def __str__(self):
        out = []
        for node in self.nodes:
            for child in node.others:
                out.append(f'{node.value} - {child.value}')
        return '\n'.join(out)

    def add_nodes(self, n1, n2):
        n1.others.append(n2)
        n2.others.append(n1)
        if n1 not in self.nodes:
            self.nodes.append(n1)
        if n2 not in self.nodes:
            self.nodes.append(n2)

    def bfs(self, start: Node, end: Node):
        predecessor = {} 
        for node in self.nodes:
            node.color = WHITE
            predecessor[node] = None
        start.color = GREY
        queue = [start]
        paths :List[List[Node]] = [] 
        while queue:
            node = queue[0]
            for child in node.others:
                if child.color == WHITE:
                    child.color = GREY
                    predecessor[child] = node
                    queue.append(child)
                if child == end:
                    print(predecessor, child)
                    path = [end]
                    n = child
                    while (parent := predecessor[n]) != start:
                        path.append(parent)
                        n = parent
                    path.append(parent)
                    paths.append(path[::-1])
            queue.pop(0)
            if node.value.islower():
                node.color = BLACK
            else:
                node.color = WHITE
        return paths

        

    def custom_df(self, start, end):
        paths = []
        seen = set()
        this_path = [start]
        done = False
        breakpoint()
        while not done:
            size = len(this_path)
            others = this_path[-1].others
            for node in others:
                key = f'{this_path[-1]}-{node}'
                if key in seen:
                    continue
                if node.value.islower() and node in this_path:
                    continue
                seen.add(key)
                this_path.append(node)
                if node == end:
                    paths.append(this_path)
                    this_path = [start]
            done = len(this_path) == size
        return paths

    def df_cormen(self, start, end):
        self.paths = []
        predecessor = {} 
        for node in self.nodes:
            node.color = WHITE
            predecessor[node] = None
        self.df_visit(start, end, predecessor)
        return self.paths

    def df_visit(self, start, end, predecessor):
        start.color = GREY
        for child in start.others:
            print(f'{child}')
            if child.color == WHITE:
                print(f'\tvisiting {start} -> {child}')
                predecessor[child] = start
                if child == end:
                    print("FOUND!***")
                    path = [end]
                    n1 = end
                    while node := predecessor.get(n1):
                        path.append(node)
                        n1 = node
                    self.paths.append(path[::-1])
                else:
                    self.df_visit(child, end, predecessor)
        start.color = BLACK

def find_paths(g, start, end):
    paths = []
    path = [start]
    to_visit = [child for child in path[-1].others]
    while to_visit:
        for child in to_visit:
            child_path = path + [child]
            if child == end:
                paths.append(child_path)


def search_children(path, node, end, paths):
    """
    >>> g, node_registry = parse_txt(SAMPLE)
    >>> paths = []
    >>> start, end = node_registry.get('start'), node_registry.get('end')
    >>> search_children([start], start, end, paths)
    """
    #print(f'**Searching {node} {path}')
    for child in node.others:
        orig_path = path[:]
        if child.value.islower() and child in path:
            continue
        path.append(child)
        if child == end:
            paths.append(path[:])
        else:
            search_children(path, child, end, paths)
        path = orig_path




def part1(txt):
    """
    >>> part1(SAMPLE)
    10
    >>> part1(SAMPLE2)
    19
    """
    g, node_registry = parse_txt(txt)
    paths = []
    start, end = node_registry.get('start'), node_registry.get('end')
    search_children([start], start, end, paths)
    print(len(paths))


def part2(txt):
    """
    >>> part2(SAMPLE)
    36
    >>> part2(SAMPLE2)
    103
    """
    g, node_registry = parse_txt(txt)
    paths = []
    start, end = node_registry.get('start'), node_registry.get('end')
    search_children_part2([start], start, end, paths)
    print(len(paths))


def search_children_part2(path, node, end, paths ):
    """
    >>> g, node_registry = parse_txt(SAMPLE)
    >>> paths = []
    >>> start, end = node_registry.get('start'), node_registry.get('end')
    >>> search_children([start], start, end, paths)
    """
    #print(f'**Searching {node} {path}')

    for child in node.others:
        orig_path = path[:]
        can_visit_small = all( v <= 1 for v in
           Counter([p.value for p in path if p.value.islower()]).values())
        if child.value == 'start':
            continue
        #print(f'{child} {path} {can_visit_small}')
        if can_visit_small:
            pass
        elif child.value.islower() and child in path:
            continue
        path.append(child)
        if child == end:
            paths.append(path[:])
        else:
            search_children_part2(path, child, end, paths)
        path = orig_path



SAMPLE = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''


SAMPLE2 = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
'''

def parse_txt(txt):
    """
    >>> g, node_registry = parse_txt(SAMPLE)
    >>> print(g)
    start - A
    start - b
    A - start
    A - c
    A - b
    A - end
    b - start
    b - A
    b - d
    b - end
    c - A
    d - b
    end - A
    end - b
    """
    nr = NodeRegistry()
    g = Graph()
    for line in (txt#.replace('start', 'START').replace('end', 'END')
        .strip().split('\n')):
        src, dst = line.split('-')
        #print(src, dst, line)
        n1 = nr.get(src)
        n2 = nr.get(dst)
        g.add_nodes(n1, n2)
    return g, nr


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print(part1(open('day12.txt').read())) # 3761
    print(part2(open('day12.txt').read())) # 99138    





    
