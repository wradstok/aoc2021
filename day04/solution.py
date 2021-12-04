import os

with open(os.getcwd() + "/day04/input.txt", mode="r", encoding="utf-8") as file:
    numbers = map(int, file.readline().split(","))

    boards, board = [], []
    while line := file.readline():
        if line == "":
            boards.append(board)

        if line == "\n":
            boards.append(board)
            board = []  # Start of a new board
            continue

        line = list(map(int, filter(None, line[:-1].split(" "))))  # Remove \n
        board.append(line)

boards = boards[1:]  # remove the empty board we created at the start


def test_winning(board):
    # Check if any row just consists of -1.
    if any(map(lambda x: x.count(-1) == len(x), board)):
        return True

    # Now check the columns.
    for i in range(len(board)):
        col = [row[i] for row in board]
        if col.count(-1) == len(col):
            return True

    return False


def calc_score(last_called, board):
    rows = [list(filter(lambda x: x != -1, row)) for row in board]
    return last_called * sum(map(sum, rows))


for called in numbers:
    # Update boards by replacing the called number with -1.
    boards_to_del = []  # Delete from consideration for part 2

    for i in range(len(boards)):
        boards[i] = [
            list(map(lambda x: -1 if x == called else x, row)) for row in boards[i]
        ]

        if test_winning(boards[i]):
            score = calc_score(called, boards[i])
            print(f"{score}")
            boards_to_del.append(i)

    for i, idx in enumerate(boards_to_del):
        del boards[idx - i]
