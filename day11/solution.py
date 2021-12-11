import os
from collections import namedtuple
from typing import Set

grid = []
with open(os.getcwd() + "/day11/input.txt") as f:
    lines = f.read().splitlines()
    for line in lines:
        grid.append(list(map(int, line)))

Point = namedtuple("Point", ["x", "y"])


def get_possible_neighbours(grid, point: Point):
    neighbours = []
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            if a == 0 and b == 0:
                continue
            pos = Point(point.x + a, point.y + b)
            if pos.x >= 0 and pos.x < len(grid[0]) and pos.y >= 0 and pos.y < len(grid):
                neighbours.append(pos)

    return neighbours


def attempt_flash(grid, point: Point, flashed: Set[Point]) -> int:
    if point in flashed or grid[point.y][point.x] < 10:
        return 0  # This point cannot flash yet.

    # Flash it up.
    flashed.add(point)
    _flashes = 1
    grid[point.y][point.x] = 0

    adjacent = get_possible_neighbours(grid, point)
    adjacent = list(filter(lambda x: x not in flashed, adjacent))

    for adj in adjacent:
        grid[adj.y][adj.x] += 1

    for adj in adjacent:
        _flashes += attempt_flash(grid, adj, flashed)

    return _flashes


flashes = 0
for i in range(1, 1000000):
    # Increment all octupus energy levels by 1.
    for y in range(len(grid)):
        grid[y] = [x + 1 for x in grid[y]]

    # Flash
    flashed = set()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            flashes += attempt_flash(grid, Point(x, y), flashed)

    if len(flashed) == sum(map(len, grid)):
        print(f"All flash on iteration {i}")
        break


print(f"Total numer of flashes {flashes}")
