import os
from collections import namedtuple
from typing import List

Point = namedtuple("Point", ["x", "y"])
Line = namedtuple("Line", ["start", "end"])

lines: List[Line] = []
with open(os.getcwd() + "/day05/input.txt") as f:
    input = f.read().splitlines()
    input = map(lambda x: x.split(" -> "), input)

    for input_line in input:
        begin, end = map(lambda x: x.split(","), input_line)
        begin, end = map(int, begin), map(int, end)
        begin, end = Point(next(begin), next(begin)), Point(next(end), next(end))
        # Swap points if in the wrong order.
        if begin > end:
            lines.append(Line(end, begin))
        else:
            lines.append(Line(begin, end))

# Determine the size of the grid.
ending = Point(max([line.end.x for line in lines]), max([line.end.y for line in lines]))

# Part 1.
grid: List[List[int]] = [[0 for _ in range(ending.x + 1)] for _ in range(ending.y + 1)]

# Draw the lines.
for line in lines:
    if line.start.x == line.end.x:
        # Horizontal position equal, so vertical line.
        for i in range(line.start.y, line.end.y + 1):
            grid[i][line.start.x] += 1
    elif line.start.y == line.end.y:
        # Vertical positions equal, so horizontal line.
        for i in range(line.start.x, line.end.x + 1):
            grid[line.start.y][i] += 1

overlapping = sum(map(lambda row: len([1 for hit in row if hit >= 2]), grid))
print(f"{overlapping} points have at least two overlapping lines.")


# Part 2
grid: List[List[int]] = [[0 for _ in range(ending.x + 1)] for _ in range(ending.y + 1)]
for line in lines:
    if line.start.x == line.end.x:
        # Horizontal position equal, so vertical line.
        for i in range(line.start.y, line.end.y + 1):
            grid[i][line.start.x] += 1
    elif line.start.y == line.end.y:
        # Vertical positions equal, so horizontal line.
        for i in range(line.start.x, line.end.x + 1):
            grid[line.start.y][i] += 1
    else:
        # Exactly 45 degrees, so it doesn't matter whether use x or y
        line_length = abs(line.end.x - line.start.x)
        for i in range(line_length + 1):
            x_dir = 1 if line.end.x > line.start.x else -1
            y_dir = 1 if line.end.y > line.start.y else -1
            grid[line.start.y + i * y_dir][line.start.x + i * x_dir] += 1

overlapping = sum(map(lambda row: len([1 for hit in row if hit >= 2]), grid))
print(f"{overlapping} points have at least two overlapping lines.")
