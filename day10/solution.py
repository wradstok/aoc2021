import os

with open(os.getcwd() + "/day10/input.txt") as f:
    lines = f.read().splitlines()


opening = ["(", "[", "{", "<"]
closing = [")", "]", "}", ">"]
corresponding = {item: closing[i] for i, item in enumerate(opening)} | {
    item: opening[i] for i, item in enumerate(closing)
}

incorrect, corrupted = [], set()
for i, line in enumerate(lines):
    stack = []
    for char in line:
        if char in opening:
            stack.append(char)
        else:
            if stack.pop() != corresponding[char]:
                incorrect.append(char)
                corrupted.add(i)
                break


scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

scores = [score * incorrect.count(item) for item, score in scores.items()]
print(sum(scores))

# Part 2.
scores = {")": 1, "]": 2, "}": 3, ">": 4}

normies = [x for i, x in enumerate(lines) if i not in corrupted]

missing_scores = []
for line in normies:
    # Process the line
    stack = []
    for char in line:
        if char in opening:
            stack.append(char)
        else:
            stack.pop()

    # Determine the missing characters
    score = 0
    while True:
        if len(stack) > 0:
            char = stack.pop()
            score = score * 5 + scores[corresponding[char]]
        else:
            missing_scores.append(score)
            break


missing_scores = sorted(missing_scores)
print(f"{missing_scores[int(len(missing_scores) / 2)]}")
