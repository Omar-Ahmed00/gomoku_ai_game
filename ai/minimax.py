import math
import time
from ai.heuristics import evaluate, AI, HUMAN, EMPTY

STATS = {
    "nodes_evaluated": 0,
    "pruning_count": 0
}

TT = {}
KILLER_MOVES = {}

def quick_order_eval(board, r, c, player):
    n = board.n
    grid = board.grid
    center = n // 2
    dist = abs(r - center) + abs(c - center)
    score = max(0, (n - dist)) * 5

    neighbor_score = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                if grid[nr][nc] == player:
                    neighbor_score += 10
                elif grid[nr][nc] == -player:
                    neighbor_score += 8

    score += neighbor_score
    return score if player == AI else -score

def order_moves(board, moves, player, heuristic_mode, depth):
    scored = []
    killers = KILLER_MOVES.get(depth, set())
    for r, c in moves:
        board.grid[r][c] = player
        s = quick_order_eval(board, r, c, player)
        if (r, c) in killers:
            s += 1000000000
        scored.append((s, (r, c)))
        board.grid[r][c] = EMPTY
    scored.sort(key=lambda x: x[0], reverse=(player == AI))
    return [m for _, m in scored]

def gen_moves(board, radius=2):
    n = board.n
    grid = board.grid
    relevant_moves = set()
    has_pieces = False

    for r in range(n):
        for c in range(n):
            if grid[r][c] != EMPTY:
                has_pieces = True
                for dr in range(-radius, radius + 1):
                    for dc in range(-radius, radius + 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == EMPTY:
                            relevant_moves.add((nr, nc))

    if not has_pieces:
        return [(n // 2, n // 2)]
    return list(relevant_moves)

def minimax(board, depth, alpha, beta, maximizing, heuristic_mode, start_time, time_limit, use_pruning=True):
    STATS["nodes_evaluated"] += 1

    key = (tuple(map(tuple, board.grid)), maximizing, depth, heuristic_mode)
    if key in TT:
        return TT[key]

    if time.time() - start_time > time_limit:
        val = evaluate(board, heuristic_mode)
        TT[key] = (val, None)
        return TT[key]

    if board.check_winner(AI):
        TT[key] = (100000000, None)
        return TT[key]
    if board.check_winner(HUMAN):
        TT[key] = (-100000000, None)
        return TT[key]

    if board.is_game_over():
        TT[key] = (0, None)
        return TT[key]

    if depth == 0:
        val = evaluate(board, heuristic_mode)
        TT[key] = (val, None)
        return TT[key]

    moves = gen_moves(board)
    if not moves:
        TT[key] = (0, None)
        return TT[key]

    if use_pruning:
        moves = order_moves(board, moves, AI if maximizing else HUMAN, heuristic_mode, depth)

    best_move = moves[0]

    if maximizing:
        max_eval = -math.inf
        for r, c in moves:
            board.grid[r][c] = AI
            eval_score, _ = minimax(
                board,
                depth - 1,
                alpha,
                beta,
                False,
                heuristic_mode,
                start_time,
                time_limit,
                use_pruning,
            )
            board.grid[r][c] = EMPTY

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (r, c)

            if use_pruning:
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    km = KILLER_MOVES.setdefault(depth, set())
                    km.add((r, c))
                    STATS["pruning_count"] += 1
                    break

        TT[key] = (max_eval, best_move)
        return TT[key]

    else:
        min_eval = math.inf
        for r, c in moves:
            board.grid[r][c] = HUMAN
            eval_score, _ = minimax(
                board,
                depth - 1,
                alpha,
                beta,
                True,
                heuristic_mode,
                start_time,
                time_limit,
                use_pruning,
            )
            board.grid[r][c] = EMPTY

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (r, c)

            if use_pruning:
                beta = min(beta, eval_score)
                if beta <= alpha:
                    km = KILLER_MOVES.setdefault(depth, set())
                    km.add((r, c))
                    STATS["pruning_count"] += 1
                    break

        TT[key] = (min_eval, best_move)
        return TT[key]
