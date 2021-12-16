
import functools

SAMPLE = '''D2FE28
'''

def hex2bin(txt:str)->str:
    """
    >>> hex2bin(SAMPLE)
    '110100101111111000101000'
    >>> hex2bin(OPERATOR1)
    '00111000000000000110111101000101001010010001001000000000'
    """
    return leftpad_byte(f'{int(txt, 16):0b}')

def leftpad_byte(txt:str, fill:int=0):
    return txt.zfill(ceiling_8(txt))

def ceiling_8(txt) -> int:
    """
    >>> ceiling_8('2')
    8
    >>> ceiling_8('2'*9)
    16
    """
    if len(txt) % 8 != 0:
        return ((len(txt) //8 ) + 1) * 8
    return len(txt)

@functools.total_ordering
class Packet:
    def __init__(self, version, pid) -> None:
        self.version = version
        self.pid = pid

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


class LiteralPacket(Packet):
    """
    >>> binstr = hex2bin(SAMPLE)
    >>> p = LiteralPacket.frombin(binstr)
    >>> p.version
    6
    >>> p.pid
    4
    >>> p.value
    2021
    >>> p.length
    21
    """
    def __init__(self, version, pid, value, length, *,
                 data=None) -> None:
        super().__init__(version, pid)
        self.value = value
        self.length = length  # length of data, not padding
        self.data = data

    @classmethod
    def frombin(cls, binstr:str):
        version = int(binstr[:3], 2)
        pid = int(binstr[3:6], 2)
        assert pid == 4
        pos = 6
        parts = []
        done = False
        while not done:#(leading := binstr[pos:pos+1]):
            data = binstr[pos+1:pos+5]
            parts.append(data)
            done = binstr[pos] == '0'
            pos += 5
        value = int(''.join(parts), 2)
        length = pos
        # if (remainder:= pos % 8) == 0:
        #     length = pos
        # else:
        #     length = pos + (8-pos%8)
        return cls(version, pid, value, length, data=binstr[:length])
    def get_version_sum(self):
        return self.version

OPERATOR1 = '''38006F45291200
'''

class OperatorPacket(Packet):
    """
    >>> binstr = hex2bin(OPERATOR1)
    >>> binstr
    '00111000000000000110111101000101001010010001001000000000'
    >>> p = OperatorPacket.frombin(binstr)
    >>> p.version
    1
    >>> p.pid
    6
    
    """

    def __init__(self, version, pid, subpackets, length,*, length_type,
                 subpacket_size=0, subpacket_data=None) -> None:
        super().__init__(version, pid)
        self.subpackets = subpackets
        self.length_type = length_type
        self.subpacket_size = subpacket_size
        self.subpacket_data = subpacket_data
        self.length = length

    @classmethod
    def frombin(cls, binstr:str , debug=False):
        if debug:
            print(f'VERSION {binstr[:3]}')
        version = int(binstr[:3], 2)
        pid = int(binstr[3:6], 2)
        assert pid != 4
        length_type = int(binstr[6:7], 2)
        subpackets = []
        subpacket_size = 0
        total_length = 0
        if length_type == 0:
            start_pos = 3 + 3 + 1 + 15
            length_pos = 3 + 3 + 1
            length = int(binstr[length_pos: length_pos + 15], 2)
            subpacket_data = binstr[start_pos:start_pos+length]
            subpackets = parse_subpackets(subpacket_data)
            subpacket_size = length
            total_length = subpacket_size + start_pos
        else:
            num_pos = 3 + 3 + 1
            num_subpackets = int(binstr[num_pos: num_pos + 11], 2)
            start_pos = 3 + 3 + 1 + 11
            subpacket_data = binstr[start_pos:]
            subpackets = parse_num_subpackets(subpacket_data, num_subpackets)
            total_length = start_pos + sum(p.length for p in subpackets)
        return OperatorPacket(version, pid, subpackets, length_type=length_type,
                              subpacket_size=subpacket_size,
                              subpacket_data=subpacket_data,
                              length=total_length)

    def get_version_sum(self):
        res = self.version
        for p in self.subpackets:
            res += p.get_version_sum()
        return res

    @property
    def value(self):
        
        if self.pid == 0:
            return sum(p.value for p in self.subpackets)
        elif self.pid == 1:
            return prod(p.value for p in self.subpackets)
        elif self.pid == 2:
            return min(p.value for p in self.subpackets)
        elif self.pid == 3:
            return max(p.value for p in self.subpackets)
        elif self.pid == 5:
            return self.subpackets[0] > self.subpackets[1]
        elif self.pid == 6:
            return self.subpackets[0] < self.subpackets[1]
        elif self.pid == 7:
            return self.subpackets[0] == self.subpackets[1]


def prod(values):
    return functools.reduce(lambda x,y:x*y, values, 1)

def parse_num_subpackets(binstr:str, num:int):
    subpackets = []
    start = 0
    pid_offset = 3
    pid_len = 3
    while len(subpackets) < num:
        pid = int(binstr[start+pid_offset: start+pid_offset+pid_len], 2)
        if pid == 4:
            subpackets.append(LiteralPacket.frombin(binstr[start:]))
        else:
            subpackets.append(OperatorPacket.frombin(binstr[start:]))
 
        start += subpackets[-1].length
    return subpackets


def parse_subpackets(binstr:str):
    subpackets = []
    done = False
    start = 0
    pid_offset = 3
    pid_len = 3
    while not done:
        pid = int(binstr[start+pid_offset: start+pid_offset+pid_len], 2)
        if pid == 4:
            subpackets.append(LiteralPacket.frombin(binstr[start:]))
        else:
            subpackets.append(OperatorPacket.frombin(binstr[start:]))

        start += subpackets[-1].length
        done = start >= len(binstr)
    return subpackets


def part1(txt):
    binstr = hex2bin(txt)
    p = OperatorPacket.frombin(binstr, debug=True)
    print(p.get_version_sum())


def part2(txt):
    binstr = hex2bin(txt)
    p = OperatorPacket.frombin(binstr, debug=True)
    print(p.value)
    
if __name__ == '__main__':
    import doctest
    #doctest.testmod()
    part1(open('day16.txt').read()) # 947
    part2(open('day16.txt').read()) # 660797830937
