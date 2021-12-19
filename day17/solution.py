import os
import math
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

with open(os.getcwd() + "/day17/input.txt") as f:
    line = f.readline().splitlines()[0]
    part = line.split("x=")[1]
    x, y = part.split(", y=")

    x = list(map(int, x.split("..")))
    y = list(map(int, y.split("..")))
    top_left = Point(x[0], y[1])
    bot_right = Point(x[1], y[0])

# Part 1.
# The highest trajectory will be when we nail the x-part of the landing zone
# i.e., the x-speed must be zero when we reach it. Since the distance travelled
# from a certain speed x is sum(x, x-1, x-2,..., 0), we can calculate it as
# x(x-1) / 2. That means we can solve for x^2 - 2x - 2 * distance = 0
# Apply ABC formula to find min&max x speed to reach the target.
def solve(distance: int):
    distance *= 2
    return int(math.sqrt(4 - 4 * distance) / 2)


min_x_speed = solve(0 - top_left.x)
max_x_speed = solve(0 - bot_right.x)

# How high can we make it go for any value between these speeds.
max_y_speed = 0
for x_speed in range(min_x_speed, max_x_speed + 1):

    # Test y speed 0, 50.
    for y_speed in range(0, 50):
        curr_speed = y_speed
        l_pos = 0
        while l_pos > bot_right.y:
            l_pos += curr_speed
            curr_speed -= 1

            # Right on the money
            if bot_right.y <= l_pos <= top_left.y:
                if y_speed > max_y_speed:
                    max_y_speed = y_speed


high_pos = sum([x for x in range(max_y_speed + 1)])
print(f"Heighest point achieved is: {high_pos}")


# Part 2, we need to check every value for x this time :(
# So lets implement the loop again.
distinct_velocities = set()
for x_speed in range(0, 300):
    for y_speed in range(-500, 500):
        curr_pos = Point(0, 0)
        curr_speed = Point(x_speed, y_speed)

        while curr_pos.y > bot_right.y and curr_pos.x < bot_right.x:
            curr_pos = Point(curr_pos.x + curr_speed.x, curr_pos.y + curr_speed.y)
            curr_speed = Point(
                curr_speed.x - 1 if curr_speed.x > 0 else 0, curr_speed.y - 1
            )

            # Right on the money.
            if (
                bot_right.y <= curr_pos.y <= top_left.y
                and top_left.x <= curr_pos.x <= bot_right.x
            ):
                distinct_velocities.add(Point(x_speed, y_speed))
print(f"Distinct # velocities to achieve target: {len(distinct_velocities)}")
