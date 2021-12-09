import os
from collections import namedtuple
from typing import List, Set

grid = []
with open(os.getcwd() + "/day09/input.txt") as f:
    lines = f.read().splitlines()
    for line in lines:
        grid.append(list(map(int, line)))

Point = namedtuple("Point", ["x", "y"])


def get_possible_neighbours(grid, point: Point):
    above = Point(point.x, point.y + 1,) if point.y < len(grid) - 1 else None
    below = Point(point.x, point.y - 1) if point.y > 0 else None
    right = Point(point.x + 1, point.y) if point.x < len(grid[point.y]) - 1 else None
    left = Point(point.x - 1, point.y) if point.x > 0 else None
    return list([x for x in [above, below, right, left] if x is not None])


def is_lowpoint(grid, point: Point):
    return all(
        map(
            lambda neighbour: grid[point.y][point.x] < grid[neighbour.y][neighbour.x],
            get_possible_neighbours(grid, point),
        )
    )


lowpoints: List[Point] = []
for y in range(len(grid)):
    for x in range(len(grid[0])):
        point = Point(x, y)
        if is_lowpoint(grid, point):
            lowpoints.append(point)

# Part 1
print(
    f"Total risk: {sum(map(lambda pos: grid[pos.y][pos.x], lowpoints)) + len(lowpoints)}"
)

# Part 2
# Every non-9 is part of exactly 1 basin. So perform dfs from every lowpoint to determine
# the content & size of each basin.
def dfs(grid, point: Point, found: Set[Point]):
    new_found = get_possible_neighbours(grid, point)
    new_found = {pos for pos in new_found if grid[pos.y][pos.x] < 9} - found
    found = found.union(new_found)
    
    for neighbour in new_found:
        found = found.union(dfs(grid, neighbour, found))
    return found


basins = []
for point in lowpoints:
    basins.append(dfs(grid, point, {point}))

largest_basins = sorted(map(len, basins), reverse=True)[0:3]
print(f"Largest basins: {largest_basins[0] * largest_basins[1] * largest_basins[2]}")
