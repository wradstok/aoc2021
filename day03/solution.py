from typing import Dict
import numpy as np
import os

# Part 1
with open(os.getcwd() + "/day03/input.txt") as file:
    binaries = file.read().splitlines()
    binaries = [list(map(int, x)) for x in binaries]

binaries: np.array = np.array(binaries)

gamma, epsilon = "", ""
for i in range(len(binaries[0])):
    col = binaries[:, i : i + 1]
    if col.sum() > len(col) / 2:
        gamma += "1"
        epsilon += "0"
    else:
        gamma += "0"
        epsilon += "1"

gamma, epsilon = int(gamma, 2), int(epsilon, 2)
print(f"{gamma * epsilon}")


# Part 2
def keep_common(readings: np.array, position: int, most_common: bool) -> np.array:
    most_common_left = sum(readings[:, position : position + 1]) >= len(readings) / 2
    most_common_left = (
        int(most_common_left) if most_common else int(not most_common_left)
    )
    keep = [x for x in readings if x[position] == most_common_left]
    return np.array(keep)


oxygen_readings, co2_readings = np.copy(binaries), np.copy(binaries)
i = 0
while len(oxygen_readings) > 1:
    oxygen_readings = keep_common(oxygen_readings, i, True)
    i += 1

i = 0
while len(co2_readings) > 1:
    co2_readings = keep_common(co2_readings, i, False)
    i += 1

oxygen = int("".join(map(str, oxygen_readings[0])), 2)
co2 = int("".join(map(str, co2_readings[0])), 2)
print(f"{oxygen * co2}")
