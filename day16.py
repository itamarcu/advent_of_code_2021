from dataclasses import dataclass
from typing import List


@dataclass
class Packet:
    version: int
    type_id: int


@dataclass
class LiteralPacket(Packet):
    value: int


@dataclass
class OperatorPacket(Packet):
    sub_packets: List['Packet']


# example packet str:
# literal 110100101111111000101000
# operator 00111000000000000110111101000101001010010001001000000000
def parse_packet(packet_str: str, starting_index: int) -> (int, Packet):
    # first three bits are the version
    index = starting_index
    version = int(packet_str[index:index + 3], 2)
    type_id = int(packet_str[index + 3:index + 6], 2)
    if type_id == 4:
        # literal packet
        number_str = ''  # for each five bits, e.g. abcde, we will keep bcde (a tells us to stop/continue)
        index += 6
        while int(packet_str[index]) == 1:
            # keep reading
            number_str += packet_str[index + 1:index + 5]
            index += 5
        # one last time
        number_str += packet_str[index + 1:index + 5]
        index += 5
        literal_number_value = int(number_str, 2)
        return index, LiteralPacket(version=version, type_id=type_id, value=literal_number_value)
    else:
        # operator packet, may have subpackets
        length_type_id = int(packet_str[index + 6])
        index += 7
        if length_type_id == 0:
            # next 15 bits are the total length in bits of sub-packets
            length_in_bits_of_subs = int(packet_str[index:index + 15], 2)
            index += 15
            sub_packets = []
            while index < starting_index + 7 + 15 + length_in_bits_of_subs:
                next_index, next_packet = parse_packet(packet_str, index)
                index = next_index
                sub_packets.append(next_packet)
            return index, OperatorPacket(version=version, type_id=type_id, sub_packets=sub_packets)
        else:
            # next 11 bits are the number of sub packets contained in this one
            number_of_subs = int(packet_str[index:index + 11], 2)
            index += 11
            sub_packets = []
            while len(sub_packets) < number_of_subs:
                next_index, next_packet = parse_packet(packet_str, index)
                index = next_index
                sub_packets.append(next_packet)
            return index, OperatorPacket(version=version, type_id=type_id, sub_packets=sub_packets)


with open('day16.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

binary_input = bin(int(lines[0], 16))[2:]
binary_input = binary_input.zfill(len(lines[0] * 4))
_, top_packet = parse_packet(binary_input, 0)

# print(top_packet)

total_version_numbers = 0


def add_up_total_version_numbers(packet: Packet):
    result = packet.version
    if isinstance(packet, OperatorPacket):
        for sub_packet in packet.sub_packets:
            result += add_up_total_version_numbers(sub_packet)
    return result


print(add_up_total_version_numbers(top_packet))


def prod(iterable):
    result = 1
    for thing in iterable:
        result *= thing
    return result

def evaluate_recursively(packet: Packet):
    if isinstance(packet, LiteralPacket):
        return packet.value
    if isinstance(packet, OperatorPacket):
        if packet.type_id == 0:
            return sum(evaluate_recursively(p) for p in packet.sub_packets)
        if packet.type_id == 1:
            return prod(evaluate_recursively(p) for p in packet.sub_packets)
        if packet.type_id == 2:
            return min(evaluate_recursively(p) for p in packet.sub_packets)
        if packet.type_id == 3:
            return max(evaluate_recursively(p) for p in packet.sub_packets)
        if packet.type_id == 5:
            first = evaluate_recursively(packet.sub_packets[0])
            second = evaluate_recursively(packet.sub_packets[1])
            return 1 if first > second else 0
        if packet.type_id == 6:
            first = evaluate_recursively(packet.sub_packets[0])
            second = evaluate_recursively(packet.sub_packets[1])
            return 1 if first < second else 0
        if packet.type_id == 7:
            first = evaluate_recursively(packet.sub_packets[0])
            second = evaluate_recursively(packet.sub_packets[1])
            return 1 if first == second else 0
        raise ValueError('weird packet operator!')
    raise ValueError('weird packet class!')

print(evaluate_recursively(top_packet))