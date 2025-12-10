import random
import time
from ai.minimax import minimax, STATS, TT, KILLER_MOVES, gen_moves
from ai.heuristics import EMPTY, evaluate, AI, HUMAN

class AIPlayer:
    def __init__(self, difficulty="medium", board_size=15):
        self.diff = difficulty.lower()
        self.board_size = board_size
        self.heuristic_mode = 2
        self.use_pruning = True

        self.configs = {
            "easy": {
                "depth": 1,
                "rand": 0.6,
                "limit": 1.0,
                "pruning": True,
                "heuristic": 1,
            },
            "medium": {
                "depth": 2,
                "rand": 0.2,
                "limit": 2.0,
                "pruning": True,
                "heuristic": 2,
            },
            "hard": {
                "depth": 3,      
                "rand": 0.0,
                "limit": 3.0,     
                "pruning": True,
                "heuristic": 2,
            },
            "adaptive": {
                "dynamic": True,
                "limit": 5.0,
                "pruning": True,
                "heuristic": 2,
            },
        }

        self.current_cfg = self.configs[self.diff]

    def adaptive_depth(self, board):
        n = board.n
        empty_cells = sum(row.count(EMPTY) for row in board.grid)
        total_cells = n * n
        filled = total_cells - empty_cells
        fill_ratio = filled / total_cells

        if fill_ratio < 0.1:
            return 1
        if fill_ratio < 0.4:
            return 2
        return 3

    def find_winning_move(self, board, player):
        moves = gen_moves(board)
        for r, c in moves:
            board.grid[r][c] = player
            if board.check_winner(player):
                board.grid[r][c] = EMPTY
                return (r, c)
            board.grid[r][c] = EMPTY
        return None

    def find_double_threat(self, board, player):
        moves = gen_moves(board)
        threat_moves = []
        for r, c in moves:
            board.grid[r][c] = player
            if board.check_winner(player):
                threat_moves.append((r, c))
            board.grid[r][c] = EMPTY
        if len(threat_moves) >= 2:
            return threat_moves[0]
        return None
    def _search_iterative_deepening(self, board, base_depth, max_depth, start_time):
        best_move = None
        best_score = None
        used_depth = base_depth

        alpha_init = -float("inf")
        beta_init = float("inf")
        for depth in range(base_depth, max_depth + 1):
            if time.time() - start_time > self.current_cfg["limit"] * 0.85:
                break

            STATS["nodes_evaluated"] = 0
            STATS["pruning_count"] = 0

            score, move = minimax(
                board,
                depth,
                alpha_init,
                beta_init,
                True,
                self.current_cfg["heuristic"],
                start_time,
                self.current_cfg["limit"],
                use_pruning=self.current_cfg["pruning"],
            )

            if move is not None:
                best_move = move
                best_score = score
                used_depth = depth
            if best_score is not None and abs(best_score) > 90_000_000:
                break
        if best_move is None:
            moves = gen_moves(board)
            if moves:
                n = board.n
                best_move = min(
                    moves,
                    key=lambda m: abs(m[0] - n // 2) + abs(m[1] - n // 2),
                )
                best_score = 0
            else:
                best_move = (board.n // 2, board.n // 2)
                best_score = 0

        return best_score, best_move, used_depth

    def get_best_move(self, board):
        n = board.n
        STATS["nodes_evaluated"] = 0
        STATS["pruning_count"] = 0
        TT.clear()
        KILLER_MOVES.clear()

        start = time.time()
        if board.move_count == 0:
            return (n // 2, n // 2)
        win = self.find_winning_move(board, AI)
        if win:
            return win
        block = self.find_winning_move(board, HUMAN)
        if block:
            return block
        fork_block = self.find_double_threat(board, HUMAN)
        if fork_block:
            return fork_block
        if self.diff == "adaptive":
            depth = self.adaptive_depth(board)
            rand_chance = 0.10
        else:
            depth = self.current_cfg.get("depth", 2)
            rand_chance = self.current_cfg.get("rand", 0.0)
        heuristic_score = evaluate(board, self.current_cfg["heuristic"])
        if self.diff != "hard":
            if abs(heuristic_score) > 20000:
                depth = min(depth + 1, 6)
            if abs(heuristic_score) > 50000:
                depth = min(depth + 2, 7)
        if self.diff != "hard" and random.random() < rand_chance:
            moves = gen_moves(board)
            if moves:
                sample = random.sample(moves, min(3, len(moves)))
                best = min(
                    sample,
                    key=lambda m: abs(m[0] - n // 2) + abs(m[1] - n // 2),
                )
                return best
        if self.diff == "hard":
            base_depth = max(3, depth)   
            max_depth = min(base_depth + 3, 7) 
            score, move, used_depth = self._search_iterative_deepening(
                board, base_depth, max_depth, start
            )
            duration = time.time() - start
            print(
                f"[HARD-ID] Move={move} Depth={used_depth} "
                f"Time={duration:.3f}s Nodes={STATS['nodes_evaluated']} "
                f"Pruned={STATS['pruning_count']}"
            )
            return move
        score, move = minimax(
            board,
            depth,
            -float("inf"),
            float("inf"),
            True,
            self.current_cfg["heuristic"],
            start,
            self.current_cfg["limit"],
            use_pruning=self.current_cfg["pruning"],
        )
        duration = time.time() - start
        print(
            f"[{self.diff.upper()}] Move={move} Depth={depth} "
            f"Time={duration:.3f}s Nodes={STATS['nodes_evaluated']} "
            f"Pruned={STATS['pruning_count']}"
        )
        return move
