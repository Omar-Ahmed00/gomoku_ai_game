# ai/minimax.py
import math
import time
from ai.heuristics import heuristic1, heuristic2, EMPTY, AI, HUMAN
TT = {}

def board_to_key(board):
    return ''.join(str(cell) for row in board.grid for cell in row)

def generate_moves_nearby(board, radius=3):
    n = board.n
    g = board.grid
    moves = set()
    any_piece = False
    for r in range(n):
        for c in range(n):
            if g[r][c] != 0:
                any_piece = True
                for dr in range(-radius, radius+1):
                    for dc in range(-radius, radius+1):
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 0:
                            moves.add((nr,nc))
    if not any_piece:
        return [(n//2, n//2)]
    return list(moves)

def order_moves(board, moves, player, mode):
    scored = []
    for (r,c) in moves:
        board.make_move(r,c, player)
        if mode == 1:
            s = heuristic1(board)
        else:
            s = heuristic2(board)
        board.undo_move(r,c)
        scored.append((s, (r,c)))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [m for _, m in scored]

def evaluate(board, mode, maximizing_player):
    if mode == 1:
        return heuristic1(board)
    else:
        return heuristic2(board)

def minimax(board, depth, alpha, beta, maximizing, mode, start_time=None, time_limit=None):
    if start_time and time_limit and (time.time() - start_time) > time_limit:
        return evaluate(board, mode, maximizing), None

    key = board_to_key(board)
    if key in TT and TT[key]['depth'] >= depth:
        return TT[key]['val'], TT[key]['move']

    if depth == 0 or board.check_winner(AI) or board.check_winner(HUMAN):
        val = evaluate(board, mode, maximizing)
        return val, None

    player = AI if maximizing else HUMAN
    moves = generate_moves_nearby(board)
    if not moves:
        return 0, None

    moves = order_moves(board, moves, player, mode)

    best_move = None
    if maximizing:
        value = -math.inf
        for (r,c) in moves:
            board.make_move(r,c, player)
            val, _ = minimax(board, depth-1, alpha, beta, False, mode, start_time, time_limit)
            board.undo_move(r,c)
            if val > value:
                value = val
                best_move = (r,c)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
    else:
        value = math.inf
        for (r,c) in moves:
            board.make_move(r,c, player)
            val, _ = minimax(board, depth-1, alpha, beta, True, mode, start_time, time_limit)
            board.undo_move(r,c)
            if val < value:
                value = val
                best_move = (r,c)
            beta = min(beta, value)
            if beta <= alpha:
                break

    TT[key] = {'val': value, 'move': best_move, 'depth': depth}
    return value, best_move

def iterative_deepening(board, max_depth, mode, time_limit=5.0):
    start = time.time()
    best = None
    for d in range(1, max_depth+1):
        val, move = minimax(board, d, -math.inf, math.inf, True, mode, start, time_limit)
        if move is not None:
            best = move
        if time.time() - start > time_limit:
            break
    return best
