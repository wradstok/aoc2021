import os
from typing import Set, Dict, List
from copy import deepcopy

caves: Dict[str, Set[str]] = {}
with open(os.getcwd() + "/day12/input.txt") as f:
    lines = f.read().splitlines()
    for line in lines:
        start, end = line.split("-")
        for item in [start, end]:
            if item not in caves:
                caves[item] = set()

        # Caves are undirected edges, so we can go back as well.
        caves[start] = caves[start].union(set([end]))
        caves[end] = caves[end].union(set([start]))


def is_big(cave: str):
    return cave == cave.upper()


def dfs(caves, path: List[str], small_visited: bool) -> List[List[str]]:
    pos = path[-1]
    adjacents = caves[pos]

    new_paths = []
    for adj in adjacents:
        if adj == "end":
            new_paths.append(path + ["end"])
        elif is_big(adj) or adj not in path:
            new_paths.extend(dfs(caves, deepcopy(path) + [adj], small_visited))
        elif adj in path and adj != "start" and not small_visited:
            new_paths.extend(dfs(caves, deepcopy(path) + [adj], True))

    return new_paths


paths = dfs(caves, ["start"], True)
print(f"There are {len(paths)} only going through small caves once.")


paths = dfs(caves, ["start"], False)
print(f"There are {len(paths)} allowing passing through 1 small cave twice.")
