import os

with open(os.getcwd() + "/day07/input.txt") as f:
    crabs = list(map(int, f.read().split(",")))


# Initial fuse use to get to position 0.
fuel_uses = [0 - crab for crab in crabs]
diffs = []

for _ in range(max(crabs)):
    diffs.append(sum(map(abs, fuel_uses)))
    fuel_uses = [fuel_use + 1 for fuel_use in fuel_uses]

print(f"{min(diffs)}")


# Part 2
diffs = []
for h_pos in range(max(crabs)):
    diff = 0
    for i, crab in enumerate(crabs):
        move = abs(crabs[i] - h_pos)
        diff += int(move * (move + 1) / 2)
    diffs.append(diff)
print(f"{min(diffs)}")
