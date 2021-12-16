import os
from collections import namedtuple
import heapq
import time

start_time = time.time()

Point = namedtuple("Point", ["x", "y"])

grid = []
with open(os.getcwd() + "/day15/input.txt") as f:
    lines = f.read().splitlines()
    for line in lines:
        grid.append(list(map(int, line)))

# Modifications for part 2.
if True:
    # First extend to the right.
    orig_width = len(grid[0])
    for y, row in enumerate(grid):
        for offset in range(0, 4):
            start, end = orig_width * offset, orig_width * (offset + 1)
            row.extend([x + 1 if x < 9 else 1 for x in row[start:end]])
    # Now extend downwards
    orig_height = len(grid)
    for offset in range(0, 4):
        start, end = orig_height * offset, orig_height * (offset + 1)
        part = list(
            map(lambda row: [x + 1 if x < 9 else 1 for x in row], grid[start:end])
        )
        grid.extend(part)


def get_adjacent(grid, point: Point):
    above = Point(point.x, point.y + 1) if point.y < len(grid) - 1 else None
    below = Point(point.x, point.y - 1) if point.y > 0 else None
    right = Point(point.x + 1, point.y) if point.x < len(grid[0]) - 1 else None
    left = Point(point.x - 1, point.y) if point.x > 0 else None
    return [x for x in [above, below, right, left] if x is not None]


def pos_in_heap(heap, point):
    # Find position of the element in the heap.
    # Return None if it is not there.
    try:
        return [y[1] for y in heap].index(point)
    except ValueError:
        return None


# Initialize data structures for dijkstra
points = {Point(x, y) for y in range(len(grid)) for x in range(len(grid[0]))}
dist = {}
for point in points:
    if point.x == 0 and point.y == 0:
        dist[point] = 0
    else:
        dist[point] = 999999

min_heap = [(0, Point(0, 0))]

# Perform dijkstra.
# We create the heap as we build it.
target = Point(len(grid[0]) - 1, len(grid) - 1)
while len(min_heap) > 0:
    _, u = heapq.heappop(min_heap)
    if u.x == -1 and u.y == -1:
        continue  # Encountered an updated item

    if u == target:
        break  # Early exit

    for adj in get_adjacent(grid, u):
        risk = dist[u] + grid[adj.y][adj.x]
        if risk < dist[adj]:
            dist[adj] = risk
            heapq.heappush(min_heap, (risk, adj))

print(f"Min distance is {dist[target]}")
