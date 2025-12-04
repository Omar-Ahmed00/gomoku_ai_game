# ai/minimax.py
import math
import time
from ai.heuristics import evaluate, AI, HUMAN, EMPTY

# Statistics global to track performance for the report
STATS = {
    "nodes_evaluated": 0,
    "pruning_count": 0
}

def order_moves(board, moves, player, heuristic_mode):
    """
    Optimization: Sort moves to check promising ones first.
    This makes Alpha-Beta pruning significantly more effective.
    """
    scored = []
    for r, c in moves:
        board.grid[r][c] = player
        # Use a quick evaluation (H1 is faster) for sorting
        score = evaluate(board, 1) 
        scored.append((score, (r, c)))
        board.grid[r][c] = EMPTY
    
    # Sort: High score first for AI, Low score first for Human
    scored.sort(key=lambda x: x[0], reverse=(player == AI))
    return [m for _, m in scored]

def gen_moves(board, radius=1):
    """
    Generates moves only around existing pieces to reduce search space.
    """
    n = board.n
    grid = board.grid
    relevant_moves = set()
    has_pieces = False
    
    for r in range(n):
        for c in range(n):
            if grid[r][c] != EMPTY:
                has_pieces = True
                for dr in range(-radius, radius+1):
                    for dc in range(-radius, radius+1):
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == EMPTY:
                            relevant_moves.add((nr, nc))
                            
    if not has_pieces:
        return [(n//2, n//2)]
        
    return list(relevant_moves)

def minimax(board, depth, alpha, beta, maximizing, heuristic_mode, start_time, time_limit, use_pruning=True):
    """
    Minimax Algorithm with Optional Alpha-Beta Pruning.
    
    Args:
        use_pruning (bool): If False, the algorithm acts as standard Minimax (for report comparison).
    """
    STATS["nodes_evaluated"] += 1

    # 1. Time Check
    if time.time() - start_time > time_limit:
        return evaluate(board, heuristic_mode), None

    # 2. Terminal Check (Win/Loss/Draw or Depth 0)
    if board.check_winner(AI): return 100000000, None
    if board.check_winner(HUMAN): return -100000000, None
    if depth == 0:
        return evaluate(board, heuristic_mode), None

    # 3. Move Generation & Ordering
    possible_moves = gen_moves(board)
    if not possible_moves: return 0, None

    # Only order moves if we are pruning (sorting helps pruning, but adds overhead for pure Minimax)
    if use_pruning:
        possible_moves = order_moves(board, possible_moves, AI if maximizing else HUMAN, heuristic_mode)

    best_move = possible_moves[0]

    if maximizing:
        max_eval = -math.inf
        for r, c in possible_moves:
            board.grid[r][c] = AI
            eval_score, _ = minimax(board, depth - 1, alpha, beta, False, heuristic_mode, start_time, time_limit, use_pruning)
            board.grid[r][c] = EMPTY

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (r, c)
            
            # --- ALPHA-BETA PRUNING LOGIC ---
            if use_pruning:
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    STATS["pruning_count"] += 1
                    break 
            # --------------------------------
            
        return max_eval, best_move

    else:
        min_eval = math.inf
        for r, c in possible_moves:
            board.grid[r][c] = HUMAN
            eval_score, _ = minimax(board, depth - 1, alpha, beta, True, heuristic_mode, start_time, time_limit, use_pruning)
            board.grid[r][c] = EMPTY

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (r, c)

            # --- ALPHA-BETA PRUNING LOGIC ---
            if use_pruning:
                beta = min(beta, eval_score)
                if beta <= alpha:
                    STATS["pruning_count"] += 1
                    break
            # --------------------------------
            
        return min_eval, best_move