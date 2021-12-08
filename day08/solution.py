import os

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
