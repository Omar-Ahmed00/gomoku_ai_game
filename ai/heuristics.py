# ai/heuristics.py

AI = 1
HUMAN = -1
EMPTY = 0
PATTERN_SCORES = {
    (5, 0): 10000000, # Win (5 in a row)
    (5, 1): 10000000,
    (5, 2): 10000000,
    (4, 2): 500000,   # Open 4 (Unstoppable)
    (4, 1): 50000,    # Blocked 4
    (3, 2): 10000,    # Open 3
    (3, 1): 1000,     # Blocked 3
    (2, 2): 500,      # Open 2
    (2, 1): 100       # Blocked 2
}

def evaluate(board, mode: int):
    """
    Wrapper to select which heuristic function to use.
    Mode 1 = Simple Heuristic (H1)
    Mode 2 = Advanced Heuristic (H2)
    """
    if mode == 1:
        return heuristic_1_simple(board)
    else:
        return heuristic_2_advanced(board)


def heuristic_1_simple(board):
    """
    H1: Simple Heuristic
    - Strategy: Purely offensive.
    - Logic: Counts how many pieces are in a row without caring much about blocks.
    - Use case: 'Easy' difficulty or baseline for report comparison.
    """
    score = 0
    n = board.n
    grid = board.grid
    center = n // 2
    for r in range(n):
        for c in range(n):
            if grid[r][c] == AI:
                score += (10 - max(abs(r-center), abs(c-center)))
            elif grid[r][c] == HUMAN:
                score -= (10 - max(abs(r-center), abs(c-center)))
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    
    for r in range(n):
        for c in range(n):
            if grid[r][c] == EMPTY: continue
            
            player = grid[r][c]
            my_score = 1 if player == AI else -1
            
            for dr, dc in directions:
                # Check 4 steps ahead
                consecutive = 0
                for k in range(1, 5):
                    nr, nc = r + dr*k, c + dc*k
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == player:
                        consecutive += 1
                    else:
                        break
                
                # Award points based on consecutive count
                if consecutive == 4: score += 10000 * my_score
                elif consecutive == 3: score += 1000 * my_score
                elif consecutive == 2: score += 100 * my_score
                elif consecutive == 1: score += 10 * my_score

    return score

def heuristic_2_advanced(board):
    """
    H2: Advanced Heuristic
    - Strategy: Offensive AND Defensive.
    - Logic: Evaluates 'Open Ends'. An open 3 is worth much more than a blocked 3.
    - Use case: 'Hard' difficulty and optimal play.
    """
    # Quick win check
    if board.check_winner(AI): return 100000000
    if board.check_winner(HUMAN): return -100000000

    score = 0
    score += eval_lines(board, AI)    # Add my potential
    score -= eval_lines(board, HUMAN) # Subtract opponent's potential
    return score

def eval_lines(board, player):
    total = 0
    n = board.n
    grid = board.grid
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    
    # We only scan lines starting at a stone to save time
    visited = set()

    for r in range(n):
        for c in range(n):
            if grid[r][c] != player: continue

            for dr, dc in directions:
                # Avoid re-scanning pieces belonging to the same line
                prev_r, prev_c = r - dr, c - dc
                if 0 <= prev_r < n and 0 <= prev_c < n and grid[prev_r][prev_c] == player:
                    continue

                # Scan the line
                stones = 0
                open_ends = 0
                
                # Check "before" the line
                if 0 <= prev_r < n and 0 <= prev_c < n and grid[prev_r][prev_c] == EMPTY:
                    open_ends += 1
                
                # Count consecutive stones
                rr, cc = r, c
                while 0 <= rr < n and 0 <= cc < n and grid[rr][cc] == player:
                    stones += 1
                    rr += dr
                    cc += dc
                
                # Check "after" the line
                if 0 <= rr < n and 0 <= cc < n and grid[rr][cc] == EMPTY:
                    open_ends += 1
                
                if stones >= 5: stones = 5
                
                total += PATTERN_SCORES.get((stones, open_ends), 0)
    
    return total