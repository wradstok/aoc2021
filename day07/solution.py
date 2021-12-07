import os

with open(os.getcwd() + "/day07/input.txt") as f:
    crabs = list(map(int, f.read()[:-1].split(",")))


# Initial fuse use.
fuel_uses = [0 - crab for crab in crabs]
diffs = []

for i in range(max(crabs)):
    diffs.append(sum(map(abs, fuel_uses)))
    fuel_uses = [fuel_use + 1 for fuel_use in fuel_uses]

print(f"{min(diffs)}")
