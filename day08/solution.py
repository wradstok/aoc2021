import os
from collections import Counter
from typing import Dict, List

with open(os.getcwd() + "/day08/input.txt") as f:
    entries = f.read().splitlines()
    signal_patterns = list(
        map(lambda x: x.split(" "), map(lambda x: x.split("|")[0].strip(), entries))
    )
    output_values = list(
        map(lambda x: x.split(" "), map(lambda x: x.split("|")[1].strip(), entries))
    )

# Map num_segments to number displayed
num_segments = {
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}

# Part 1.
count = 0
for output_line in output_values:
    for output_value in output_line:
        if len(output_value) in num_segments.keys():
            count += 1

print(f"Digits 1,4,7 or 8 occur {count} times")

# Part 2.
def number_to_letters():
    return {
        0: "abcefg",
        1: "cf",
        2: "acdeg",
        3: "acdfg",
        4: "bcdf",
        5: "abdfg",
        6: "abdefg",
        7: "acf",
        8: "abcdefg",
        9: "abcdfg",
    }


def determine_remaining_info(mapping: Dict, input: List[str]):
    remaining = [x for x in input if x not in mapping.values()]
    letter_counts = Counter("".join(remaining))
    return remaining, letter_counts


def determine_mapping(input):
    mapping = {
        1: next((x for x in input if len(x) == 2)),
        4: next((x for x in input if len(x) == 4)),
        7: next((x for x in input if len(x) == 3)),
        8: next((x for x in input if len(x) == 7)),
    }

    remaining, letter_counts = determine_remaining_info(mapping, input)

    letter_mapping = {
        "a": None,  # solved
        "b": None,
        "c": None,
        "d": None,
        "e": next(
            (k for k, v in letter_counts.items() if v == 3)
        ),  # Only one which occurs 3 times
        "f": None,
        "g": None,  # solved
    }

    # Only 'g' and 'a' are in all remaining letters.
    # Of these, 'a' occurs in 7, and 'g' does not
    options = [k for k, v in letter_counts.items() if v == 6]
    letter_mapping["a"] = options[0] if options[0] in mapping[7] else options[1]
    letter_mapping["g"] = options[1] if options[0] in mapping[7] else options[0]

    # From the remaining figures, remove the letters we already have for those with
    # 5 items displayed. We get 3 options: 2, 3 and 5. Only 2 has 2 letters remaining.
    # These are 'c' and 'd'. 'c' occurs in 7, and 'd' does not.
    options = list(
        list(
            filter(
                lambda x: len(x) == 2,
                map(
                    lambda x: set(x)
                    - {v for k, v in letter_mapping.items() if v is not None},
                    [x for x in remaining if len(x) == 5],
                ),
            )
        )[0]
    )
    letter_mapping["c"] = options[0] if options[0] in mapping[7] else options[1]
    letter_mapping["d"] = options[1] if options[0] in mapping[7] else options[0]

    # We only have 'b' and 'f' left to map. Furthermore, we know that 'f' is in 1.
    # Therefore, we find 'f' by checking which letter in 1 we were missing,
    # and find 'b' as the last remaining letter.
    letter_mapping["f"] = [x for x in mapping[1] if x not in letter_mapping.values()][0]
    letter_mapping["b"] = [
        x for x in letter_mapping.keys() if x not in letter_mapping.values()
    ][0]

    # Turn out letter mapping into number codes.
    decoding = {}
    for numb, letters in number_to_letters().items():
        decoding[numb] = {letter_mapping[letter] for letter in letters}

    return decoding


decoding = determine_mapping(signal_patterns[0])


results = []
for i in range(len(entries)):
    decoding = determine_mapping(signal_patterns[i])
    output = list(map(set, output_values[i]))

    local_res = ""
    for signal in output:
        decoded = next((numb for numb, sign in decoding.items() if sign == signal))
        local_res += str(decoded)

    results.append(local_res)

print(f"Sum of all outputs {sum(map(int, results))}")
