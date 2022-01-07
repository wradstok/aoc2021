import os
import ast
from collections import namedtuple
from enum import Enum
from typing import List, Tuple

PathValue = namedtuple("PathValue", ["value", "path"])

# I could have been reasonable and implemented a binary tree.
# Instead, I tried to operate on the list directly.
# This was a bad idea.
with open(os.getcwd() + "/day18/test.txt") as f:
    problems = list(map(ast.literal_eval, f.read().splitlines()))


def depth(problem: List) -> Tuple[List, int]:
    items = []
    for i, subproblem in enumerate(problem):
        if isinstance(subproblem, List):
            path, dep = depth(subproblem)
            items.append(([i] + path, dep + 1))

    if len(items) == 0:
        return [], 0

    return max(items, key=lambda x: x[1])


def find_large(problem):
    for i, subproblem in enumerate(problem):
        if isinstance(subproblem, List):
            path = find_large(subproblem)
            if path is not None:
                return [i] + path
        elif subproblem >= 10:
            return [i]

    return None


def traverse(problem: List, path: List):
    for idx in path:
        problem = problem[idx]
    return problem


class Side(Enum):
    left = -1
    middle = 0
    right = 1


def find_closest(
    problem: PathValue, target_path: List, side: Side
) -> Tuple[PathValue, PathValue]:
    if isinstance(problem.value, int):
        if side == Side.right:
            return None, problem
        if side == Side.left:
            return problem, None
        raise ValueError

    # Reached the bottom
    if isinstance(problem.value[0], int) and isinstance(problem.value[1], int):
        return None, None

    right = PathValue(problem.value[1], problem.path + [1])
    left = PathValue(problem.value[0], problem.path + [0])

    if side == Side.right:
        return find_closest(left, target_path, side)
    if side == Side.left:
        return find_closest(right, target_path, side)

    # We are on the path.
    next_side = target_path[len(problem.path)]
    next_path = PathValue(problem.value[next_side], problem.path + [next_side])
    left_ret, right_ret = find_closest(next_path, target_path, Side.middle)

    # If we found nothing from the middle, find it from further out
    if next_side == 0 and right_ret is None:
        # if right.path != target_path:
        _, right_ret = find_closest(right, target_path, Side.right)
    if next_side == 1 and left_ret is None:
        # if left.path != target_path:
        left_ret, _ = find_closest(left, target_path, Side.left)

    return left_ret, right_ret


def modify(problem, path, value) -> List:
    if len(path) == 0:
        return value

    curr, remaining = path[0], path[1:]
    if curr == 1:
        # Rebuild on right
        return [problem[0], modify(problem[1], remaining, value)]

    # Rebuild on left
    return [modify(problem[0], remaining, value), problem[1]]


def explode(problem: List) -> List:
    path, max_depth = depth(problem)
    if max_depth >= 4:
        item = traverse(problem, path)
        left, right = find_closest(PathValue(problem, []), path, Side.middle)

        problem = modify(problem, path, 0)
        if left is not None:
            problem = modify(problem, left.path, left.value + item[0])
        if right is not None:
            problem = modify(problem, right.path, right.value + item[1])

    return problem


def split(problem: List) -> List:
    path = find_large(problem)
    if path is None:
        return problem
    value = traverse(problem, path)
    problem = modify(problem, path, [int(value / 2), int(value / 2 + 1)])
    return problem


def reduce(problem):
    while True:
        n_problem = explode(problem)
        if n_problem == problem:
            break
        problem = n_problem

    n_problem = split(problem)
    if n_problem == problem:
        return problem
    return reduce(n_problem)


def magnitude(problem: List) -> int:
    if isinstance(problem, List):
        return 3 * magnitude(problem[0]) + 2 * magnitude(problem[1])
    return problem


# for problem in problems:
local = problems[0]

# print(reduce(local))

for i in range(1, len(problems)):
    res = [local, problems[i]]
    res = reduce(res)
    print(res)
    print(magnitude(res))
    local = res
