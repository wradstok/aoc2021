# Part 1
with open("input.txt") as file:
    depths = list(map(int, file.readlines()))

previous = depths[0]
larger = 0
for depth in depths:
    if depth > previous:
        larger += 1
    previous = depth
print(f"Part 1: {larger} measurements are larger than the previous.")

# Voor als we gek willen doen
print(f"{[y > x for x, y in zip(depths, depths[1:])].count(True)}")
print(f"{len([1 for x, y in zip(depths, depths[1:]) if y > x])}")


# Part 2
window_size = 3
previous = sum(depths[0:3]) 
larger = 0
for i in range(len(depths) - window_size + 1):
    depth = sum(depths[i:i + window_size])
    if depth > previous:
        larger += 1
    previous = depth

print(f"Part 2: {larger} measurements are larger than the previous.")

# Voor als we gek willen doen
items = (depths[x:] for x in range(window_size))
window_depths = list(map(sum, zip(*items)))
result = [y > x for x, y in zip(window_depths, window_depths[1:])].count(True)
print(f"{result}")