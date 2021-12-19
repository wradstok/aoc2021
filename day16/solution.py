import os
from packet import Packet

with open(os.getcwd() + "/day16/input.txt") as f:
    line = f.readline().splitlines()[0]

# Parse binary. Don't forget to pad on the left side.
binary = list("".join(map(lambda x: format(int(x, 16), "04b"), line)))

packet = Packet(binary)

print(f"Version sum: {packet.get_version_sum()}")
print(f"Total value: {packet.get_value()}")
