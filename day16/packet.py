from typing import List
from functools import reduce

def take(binary: List[str], amount: int, parse: bool = True) -> str | int:
    res = ""
    for _ in range(amount):
        res += binary.pop(0)

    return to_int(res) if parse else list(res)

def to_int(binary: List[str] | str) -> int:
    if isinstance(binary, List): 
        binary = "".join(binary)
    return int(binary, 2)

class Packet:
    version: int
    id: int 
    subpackets: List['Packet']
    literal: int

    def __init__(self, binary: List[str]) -> None:
        self.version = take(binary, 3)
        self.id = take(binary, 3)
        self.literal = -1
        self.subpackets = []

        match int(self.id):
            case 4:
                literal = []
                while True:
                    start, bitstr = take(binary, 1), take(binary, 4, False)
                    literal.extend(bitstr)
                    if start == 0:
                        break
                self.literal = to_int(literal)
   
            case _:
                length_type_id = take(binary, 1)

                if length_type_id == 0:
                    length = take(binary, 15)
                    section_to_parse = take(binary, length, False)
                    while len(section_to_parse) > 0:
                        self.subpackets.append(Packet(section_to_parse))

                elif length_type_id == 1:
                    num_subpackets = take(binary, 11)
                    for _ in range(num_subpackets):
                        self.subpackets.append(Packet(binary))

                else:
                    raise ValueError
    
    def get_version_sum(self):
        return self.version + sum([p.get_version_sum() for p in self.subpackets])

    def get_value(self) -> int:
        sub_values = [p.get_value() for p in self.subpackets]
        match self.id:
            case 0:
                return sum(sub_values)
            case 1:
                if len(sub_values) == 1:
                    return sub_values[0]
                return reduce(lambda x, y: x * y, sub_values)
            case 2:
                return min(sub_values)
            case 3:
                return max(sub_values)
            case 4:
                return self.literal
            case 5:
                return 1 if sub_values[0] > sub_values[1] else 0
            case 6:
                return 1 if sub_values[0] < sub_values[1] else 0
            case 7:
                return 1 if sub_values[0] == sub_values[1] else 0
            case _:
                raise ValueError
