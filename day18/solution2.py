import os
import ast
from typing import List, Optional, Tuple, NamedTuple, Union

class Leaf(NamedTuple):
    left: int
    right: int
    parent: 'Node'

class Node(NamedTuple):
    left : Union['Node',Leaf]
    right : Union['Node',Leaf]
    parent: Optional['Node']

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


def find_closest(problem: List, curr_path: List, target_path: List, on_left: Optional[bool]) -> Tuple[int, List]:
    left, left_path = problem[0], curr_path + [0]
    right, right_path = problem[1], curr_path + [1]


    def check(item, item_path, target_path, on):
        if isinstance(item, int):
            return item, item_path
        return find_closest(item, item_path, target_path, on)

    
    shortest_path = min(len(curr_path), len(target_path))
    if all(curr_path[idx] == target_path[idx] for idx in range(shortest_path)):
        next_side = target_path[shortest_path]
        
        # return check(problem[next_side], curr_path + [next_side], target_path, None)

        if next_side == 0:
            # If we go left, return the closest value on the right.
            return check(left, left_path, target_path, True)
        else:
            # If we go right, return the closest value on the left.
            return check(right, right_path, target_path, False)

    
    if on_left:       # On the left side of the target, find the rightmost value.
        return check(left, left_path, target_path, True)
    else:
        return check(right, right_path, target_path, )
    # Can we find something on the left hand side.
    left, left_path = find_closest(left, left_path, target_path)
    if left != None:
        return left, left_path

    # Try to find it on the right
    return find_closest(right, right_path, target_path)


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
        left, path_left = find_closest(problem, [0], path)
        right, path_right = find_closest(problem, [1], path)

        problem = modify(problem, path, 0)
        if left != None:
            problem = modify(problem, path_left, left + item[0])
        if right != None:
            problem = modify(problem, path_right, right + item[1])

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

print(reduce(local))

for i in range(1, len(problems)):
    res = [local, problems[i]]
    res = reduce(res)
    print(res)
    print(magnitude(res))
    local = res