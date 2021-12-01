
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
def comp_tuple(tup):
    return tup[1] > tup[0]
print(f"{len(list(filter(comp_tuple, zip(depths, depths[1:]))))}")

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
result = filter(comp_tuple, zip(window_depths, window_depths[1:]))
print(f"{len(list(result))}")


