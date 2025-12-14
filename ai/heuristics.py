AI = 1
HUMAN = -1
EMPTY = 0

PATTERN_SCORES = {
    (5, 0): 10000000,
    (5, 1): 10000000,
    (5, 2): 10000000,
    (4, 2): 500000,
    (4, 1): 50000,
    (4, 0): 1000,
    (3, 2): 10000,
    (3, 1): 1000,
    (3, 0): 50,
    (2, 2): 500,
    (2, 1): 100,
    (2, 0): 5,
}

def evaluate(board, mode: int):
    if mode == 0:
        return simple_center_bias(board)
    elif mode == 1:
        return heuristic_1_simple(board)
    else:
        return heuristic_2_advanced(board)
def heuristic_1_simple(board):
    score = 0
    n = board.n
    grid = board.grid
    center = n // 2

    for r in range(n):
        for c in range(n):
            if grid[r][c] == AI:
                d = max(abs(r - center), abs(c - center))
                score += (12 - d) * 10
            elif grid[r][c] == HUMAN:
                d = max(abs(r - center), abs(c - center))
                score -= (12 - d) * 10

    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(n):
        for c in range(n):
            if grid[r][c] == EMPTY:
                continue

            p = grid[r][c]
            m = 1 if p == AI else -1

            for dr, dc in dirs:
                cons = 1

                for k in range(1, 5):
                    nr, nc = r + dr * k, c + dc * k
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == p:
                        cons += 1
                    else:
                        break

                for k in range(1, 5):
                    nr, nc = r - dr * k, c - dc * k
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == p:
                        cons += 1
                    else:
                        break

                if cons >= 5:
                    score += 100000 * m
                elif cons == 4:
                    score += 1000 * m
                elif cons == 3:
                    score += 100 * m
                elif cons == 2:
                    score += 10 * m

    return score

def heuristic_2_advanced(board):
    if board.check_winner(AI):
        return 100000000
    if board.check_winner(HUMAN):
        return -100000000
    return eval_lines(board, AI) - eval_lines(board, HUMAN)

def eval_lines(board, player):
    total = 0
    n = board.n
    grid = board.grid
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    center = n // 2

    for r in range(n):
        for c in range(n):
            if grid[r][c] != player:
                continue

            for dr, dc in dirs:
                pr, pc = r - dr, c - dc
                if 0 <= pr < n and 0 <= pc < n and grid[pr][pc] == player:
                    continue

                stones = 0
                open_ends = 0

                if 0 <= pr < n and 0 <= pc < n and grid[pr][pc] == EMPTY:
                    open_ends += 1

                rr, cc = r, c
                while 0 <= rr < n and 0 <= cc < n and grid[rr][cc] == player:
                    stones += 1
                    rr += dr
                    cc += dc

                if 0 <= rr < n and 0 <= cc < n and grid[rr][cc] == EMPTY:
                    open_ends += 1

                if stones >= 5:
                    stones = 5

                base = PATTERN_SCORES.get((stones, open_ends), 0)

                if player == HUMAN:
                    base *= 1.4
                    if stones == 4 and open_ends >= 1:
                        base += 5000000
                    if stones == 3 and open_ends == 2:
                        base += 1200000
                    if stones == 2 and open_ends == 2:
                        base += 12000

                d = abs(r - center) + abs(c - center)
                base += max(0, (12 - d) * 4)

                total += base

    return total
def simple_center_bias(board):
    score = 0
    n = board.n
    center = n // 2

    for r in range(n):
        for c in range(n):
            if board.grid[r][c] == AI:  
                score += 5 - max(abs(r - center), abs(c - center))
            elif board.grid[r][c] == HUMAN:  
                score -= 5 - max(abs(r - center), abs(c - center))

    return score