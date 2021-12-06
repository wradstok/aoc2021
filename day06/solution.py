import os
from collections import Counter

NUM_DAYS = 256
with open(os.getcwd() + "/day06/input.txt") as f:
    lanternfish = f.readline().splitlines()[0].split(",")
    lanternfish = map(int, lanternfish)
    lanternfish = Counter(lanternfish)

for _ in range(NUM_DAYS):
    next_iter = Counter({day: 0 for day in lanternfish.keys()})
    for days, num_fish in lanternfish.items():
        if days == 0:
            next_iter[8] = num_fish
            next_iter[6] = num_fish
        else:
            next_iter[days - 1] += num_fish

    lanternfish = next_iter

print(f"There are {lanternfish.total()} lanternfish on day {NUM_DAYS}")
