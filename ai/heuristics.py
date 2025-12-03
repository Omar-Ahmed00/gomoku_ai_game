# ai/heuristics.py
AI = 1
HUMAN = -1
EMPTY = 0


SCORES = {
    (5, 2): 1000000,    
    (4, 2): 100000,     
    (4, 1): 10000,      
    (3, 2): 5000,    
    (3, 1): 500,        
    (2, 2): 200,    
    (2, 1): 50,      
}

def in_bounds(n, r, c):
    return 0 <= r < n and 0 <= c < n

def scan_five_segment(grid, r, c, dr, dc, n):
    seg = []
    for i in range(5):
        rr = r + i*dr
        cc = c + i*dc
        if not in_bounds(n, rr, cc):
            return None
        seg.append(grid[rr][cc])
    return seg

def classify_segment(segment, player):
    player_count = segment.count(player)
    opponent = HUMAN if player == AI else AI
    if opponent in segment:
        pass
    return player_count, segment.count(EMPTY)

def evaluate_board_by_lines(board, player):
    n = board.n
    g = board.grid
    total = 0
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for dr,dc in dirs:
        for r in range(n):
            for c in range(n):
                seg = scan_five_segment(g, r, c, dr, dc, n)
                if seg is None:
                    continue
                if player == AI:
                    me = AI
                    opp = HUMAN
                else:
                    me = HUMAN
                    opp = AI

                if opp in seg and me in seg:
                    continue 

                cnt = seg.count(me)
                empty_cnt = seg.count(EMPTY)
                if cnt == 0:
                    continue
                before_r, before_c = r - dr, c - dc
                after_r, after_c = r + 5*dr, c + 5*dc
                open_ends = 0
                if in_bounds(n, before_r, before_c):
                    if g[before_r][before_c] == EMPTY:
                        open_ends += 1
                else:
                    pass
                if in_bounds(n, after_r, after_c):
                    if g[after_r][after_c] == EMPTY:
                        open_ends += 1

                key = (cnt, open_ends)
                add = SCORES.get(key, 0)
                total += add if me == AI else -add
    return total

def center_control_bonus(board, player):
    n = board.n
    center_r, center_c = n//2, n//2
    bonus = 0
    for r in range(n):
        for c in range(n):
            if board.grid[r][c] == player:
                dist = abs(r-center_r) + abs(c-center_c)
                bonus += max(0, 10 - dist)  # tunable
    return bonus

def heuristic2(board):
    if board.check_winner(AI):
        return 10**9
    if board.check_winner(HUMAN):
        return -10**9

    score = 0
    score += evaluate_board_by_lines(board, AI)
    score -= evaluate_board_by_lines(board, HUMAN)
    score += center_control_bonus(board, AI) * 5
    score -= center_control_bonus(board, HUMAN) * 5
    return score

def heuristic1(board):
    n = board.n
    grid = board.grid
    score = 0
    for r in range(n):
        for c in range(n):
            if grid[r][c] == AI:
                score += 10
            elif grid[r][c] == HUMAN:
                score -= 10
    for r in range(n):
        for c in range(n):
            if grid[r][c] != 0:
                continue
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr==0 and dc==0: continue
                    nr, nc = r+dr, c+dc
                    if in_bounds(n,nr,nc):
                        if grid[nr][nc] == AI:
                            score += 1
                        elif grid[nr][nc] == HUMAN:
                            score -= 1
    return score
