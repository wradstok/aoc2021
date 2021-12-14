import os
from typing import Set, Dict, List
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
Fold = namedtuple("Fold", ["axis", "pos"])

dots: Set[Point] = set()
folds: List[Fold] = []
with open(os.getcwd() + "/day13/input.txt") as f:
    lines = f.read().splitlines()

    for line in lines:
        if len(line) == 0:
            continue
        if line.startswith("fold"):
            start, end = line.split("=")
            folds.append(Fold(start[-1], int(end)))
        else:
            x, y = line.split(",")
            dots.add(Point(int(x), int(y)))


for i, fold in enumerate(folds):
    print(f"After {i} folds there are {len(dots)} dots")

    if fold.axis == "y":
        keep = {dot for dot in dots if dot.y < fold.pos}
        for dot in dots - keep:
            offset = dot.y - fold.pos
            keep.add(Point(dot.x, fold.pos - offset))
    elif fold.axis == "x":
        keep = {dot for dot in dots if dot.x < fold.pos}
        for dot in dots - keep:
            offset = dot.x - fold.pos
            keep.add(Point(fold.pos - offset, dot.y))

    dots = keep

# Print the pattern.
x_max, y_max = max([point.x for point in dots]), max([point.y for point in dots])
for y in range(y_max + 1):
    line = ""
    for x in range(x_max + 1):
        line += "#" if Point(x, y) in dots else "."
    print(line)
