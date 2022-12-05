# this is all very bad code.
from copy import deepcopy
from typing import Union, Optional
import os
import ast
from math import floor, ceil

class Pair:
    left: Union["Pair", int]
    right: Union["Pair", int]
    depth: int
    parent: Optional["Pair"]

    def __init__(self, items: list, depth: int = 0, parent: Optional["Pair"] = None):
        self.parent = parent
        self.depth = depth

        l, r = items[0], items[1]
        if type(l) == int:
            self.left = l
        elif type(l) == list:
            self.left = Pair(l, depth + 1, self)
        else:
            self.left = items[0]

        if type(r) == int:
            self.right = r
        elif type(r) == list:
            self.right = Pair(r, depth + 1, self)
        else:
            self.right = items[1]

    def magnitude(self):
        left = 3 * self.left if type(self.left) == int else 3 * self.left.magnitude()
        right = 2 * self.right if type(self.right) == int else 2 * self.right.magnitude()
        return left + right
         
    def split(self, val: int) -> "Pair":
        return Pair([floor(val / 2), ceil(val / 2)], self.depth + 1, self)

    def kill(self, child: "Pair"):
        if self.left is child:
            self.left = 0
        if self.right is child:
            self.right = 0
        
    def try_explode(self) -> bool:
        if self.depth == 4:
            assert self.parent is not None and isinstance(self.right, int) and isinstance(self.left, int) # silence mypy
            res = find_nearest_right(self)
            if res is not None:
                node, side = res
                if side == "L":
                    node.left += self.right
                else:
                    node.right += self.right
            # Left num
            res = find_nearest_left(self)
            if res is not None:
                node, side = res
                if side == "L":
                    node.left += self.left
                else:
                    node.right += self.left

            self.parent.kill(self)
            return True
            
        res = False
        if type(self.left) == Pair:
            res = self.left.try_explode()
        
        if not res and type(self.right) == Pair:
            res = self.right.try_explode()

        return res

    def try_split(self):
        if isinstance(self.left, int) and self.left > 9:
            self.left = self.split(self.left)
            return True

        if isinstance(self.left, Pair) and self.left.try_split():
            return True

        if isinstance(self.right, int) and self.right > 9 :
            self.right = self.split(self.right)
            return True

        return isinstance(self.right, Pair) and self.right.try_split()

    def rreduce(self) -> bool:
        exploded = self.try_explode()
        if exploded:
            return True
    
        if self.try_split():
            return True

        if type(self.left) == Pair:
            res = self.left.rreduce()
            if not res and type(self.right) == Pair:
                res = self.right.rreduce()
            return res

        return False
        
    def inc_depth(self):            
        self.depth += 1
        if type(self.left) != int:
            self.left.inc_depth()
        if type(self.right) != int:
            self.right.inc_depth()
    
    def create_list(self) -> list:
        left = self.left if type(self.left) == int else self.left.create_list()
        right = self.right if type(self.right) == int else self.right.create_list()
        return [left, right]

def find_nearest_right(node: Pair) -> Optional[tuple[Pair, str]]:
    if node.parent is None:
        return None
    
    if node.parent.right == node:
        return find_nearest_right(node.parent)
    
    if isinstance(node.parent.right, int):
        return node.parent, "R"

    res = find_leftmost(node.parent.right)
    if res is None:
        return res
    return res, "L"


def find_nearest_left(node: Pair) -> Optional[tuple[Pair, str]]:
    if node.parent is None:
        return None
    
    if node.parent.left == node:
        return find_nearest_left(node.parent)
    
    if isinstance(node.parent.left, int):
        return node.parent, "L"

    res = find_rightmost(node.parent.left)
    if res is None:
        return res
    return res, "R"

def find_leftmost(node: Pair):
    if type(node.left) == Pair:
        return find_leftmost(node.left)
    return node

def find_rightmost(node: Pair):
    if type(node.right) == Pair:
        return find_rightmost(node.right)
    return node

def add_pairs(left: Pair, right: Pair) -> Pair:
    new = Pair([left, right])
    left.parent = new
    right.parent = new
    left.inc_depth()
    right.inc_depth()

    while new.rreduce():
        pass
    return new

# Part 1
with open(os.getcwd() + "/day18/input.txt") as f:
    problem_lists = list(map(ast.literal_eval, f.read().splitlines()))
    problems = [Pair(problem) for problem in problem_lists]

local = problems[0]
for problem in problems[1:]:
    local = add_pairs(local, problem)
print(local.magnitude())    

# Part 2
# I made the data structure mutable. Oops. So just re-read the input every time
# This is so bad. I'm so sorry. 
highest = 0
for i in range(len(problems)):
    with open(os.getcwd() + "/day18/input.txt") as f:
        problem_lists = list(map(ast.literal_eval, f.read().splitlines()))
        problems = [Pair(problem) for problem in problem_lists]

    for problem in problems:
        if problems[i] == problem:
            continue
        cpy = deepcopy(problems[i])
        res = add_pairs(cpy, problem).magnitude()
        if res > highest:
            highest = res

print(highest)