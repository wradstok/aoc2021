import os
import re
from collections import namedtuple, Counter
from copy import deepcopy

with open(os.getcwd() + "/day14/input.txt") as f:
    lines = f.read().splitlines()
    polymer = lines[0]

    rules = {}
    for line in lines[2:]:
        pattern, target = line.split(" -> ")
        rules[pattern] = target

Insertion = namedtuple("insertion", ["char", "pos"])

# Part 1: actually model the strings
for step in range(1, 11):
    insertions = []
    for pattern, target in rules.items():
        local = [
            Insertion(target, match.start() + 1)
            for match in re.finditer(f"(?={pattern})", polymer)
        ]
        insertions.extend(local)
    insertions = sorted(insertions, key=lambda x: x.pos)

    for offset, insertion in enumerate(insertions):
        position = offset + insertion.pos
        polymer = polymer[0:position] + insertion.char + polymer[position:]


occs = Counter(polymer)
print(f"After 10 iterations: {max(occs.values()) - min(occs.values())}")

# Part 2: original approach is WAY too slow to work for 40 iterations..
polymer = lines[0]
occs = Counter(
    {
        pattern: sum([1 for _ in re.finditer(f"(?={pattern})", polymer)])
        for pattern, _ in rules.items()
    }
)
letters = Counter(polymer)
for step in range(1, 41):
    # Copy the current state: everything is processed at once.
    temp_occs = deepcopy(occs)

    found_patterns = [pattern for pattern in rules.keys() if temp_occs[pattern] > 0]
    for pattern in found_patterns:
        # Increase target letter count.
        target = rules[pattern]
        letters[target] += temp_occs[pattern]

        # Create & count resulting patterns
        left = pattern[0] + target
        right = target + pattern[1]
        for new_pattern in [left, right]:
            occs[new_pattern] += temp_occs[pattern]

        # Current pattern doesn't exist anymore.
        occs[pattern] -= temp_occs[pattern]


print(f"After 40 iterations: {max(letters.values()) - min(letters.values())}")
