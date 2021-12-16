import pytest
import day16

def test_parse_operator():
    OPERATOR1 = '''38006F45291200
'''
    binstr = day16.hex2bin(OPERATOR1)
    p = day16.OperatorPacket.frombin(binstr, debug=True)
    assert p.version == 1
    assert p.pid == 6
    assert p.length_type == 0
    assert p.subpacket_size == 27
    assert p.subpacket_data == '1101000101001010010001001000000000'

def test_parse_subpackets():
    data = '1101000101001010010001001000000000'
    subs = day16.parse_subpackets(data)
    lit = subs[0]
    assert lit.version == 6
    assert lit.pid == 4
    assert lit.value == 10
    assert lit.length == 11
    assert len(subs) == 2
    lit2 = subs[1]
    assert lit2.version == 2
    assert lit2.pid == 4
    assert lit2.value == 20
    assert lit2.length == 16

OP2 = 'EE00D40C823060'
def test_parse_op2():
    binstr = day16.hex2bin(OP2)
    p = day16.OperatorPacket.frombin(binstr, debug=True)
    assert p.version == 7
    assert p.pid == 3
    assert p.length_type == 1
    assert len(p.subpackets) == 3
    p1 = p.subpackets[0]
    assert p1.version == 2
    assert p1.pid == 4
    assert p1.value == 1
    assert p1.length == 11
    assert p1.data == '01010000001' 
    p2 = p.subpackets[1]
    assert p2.data == '10010000010'
    assert p2.version == 4
    assert p2.pid == 4
    assert p2.value == 2
    assert p2.length == 11
    p3 = p.subpackets[2]
    assert p3.data == '00110000011'
    assert p3.version == 1
    assert p3.pid == 4
    assert p3.value == 3
    assert p3.length == 11


OP3 = '8A004A801A8002F478'
def test_parse_op3():
    binstr = day16.hex2bin(OP3)
    p = day16.OperatorPacket.frombin(binstr, debug=True)
    assert p.version == 4
    assert p.subpackets[0].version == 1
    assert p.subpackets[0].subpackets[0].version == 5
    assert p.subpackets[0].subpackets[0].subpackets[0].version == 6
    assert p.subpackets[0].subpackets[0].subpackets[0].value == 15



OP4 = '620080001611562C8802118E34'
def test_parse_op3():
    binstr = day16.hex2bin(OP4)
    p = day16.OperatorPacket.frombin(binstr, debug=True)
    assert p.get_version_sum() == 12


@pytest.mark.parametrize('hexstr, res',
                         [('8A004A801A8002F478', 16),
                         ('620080001611562C8802118E34', 12),
                         ('C0015000016115A2E0802F182340', 23),
                         ('A0016C880162017C3686B18A3D4780', 31)],
                         )
def test_version_sums(hexstr, res):
    binstr = day16.hex2bin(hexstr)
    p = day16.OperatorPacket.frombin(binstr, debug=True)
    assert p.get_version_sum() == res



