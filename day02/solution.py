# Part 1
with open("input.txt") as file:
    commands = list(map(lambda x: x.split(), file.read().splitlines()))

pos_h, pos_v = 0,0
for direction, amount in commands:
    amount = int(amount)
    if direction == "forward":
        pos_h += amount
    elif direction == "down":
        pos_v += amount
    elif direction == "up":
        pos_v -= amount

print(f"Position {pos_v * pos_h}")

pos_h, pos_v, aim = 0,0,0
for direction, amount in commands:
    amount = int(amount)
    if direction == "forward":
        pos_h += amount
        pos_v += aim * amount
    elif direction == "down":
        aim += amount
    elif direction == "up":
        aim -= amount

print(f"Position {pos_v * pos_h}")
