
import time
import random
from ai.minimax import minimax, iterative_deepening
from ai.heuristics import AI, HUMAN, EMPTY


class AIPlayer:
    def __init__(self, depth=None, mode=None, difficulty="easy", heuristic=None):

        self.difficulty = difficulty.lower() if isinstance(difficulty, str) else "easy"

        self.heuristic_map = {
            "Simple": 1,
            "Pattern": 2,
            "Advanced": 3,
            "Dynamic": 4
        }

        if heuristic is not None and heuristic in self.heuristic_map:
            mode_from_gui = self.heuristic_map[heuristic]
        else:
            mode_from_gui = mode  

        # DIFFICULTY PRESETS
        difficulty_config = {
            "easy":    {"depth": 1, "heuristic": 1, "time": 0.2, "block": False, "win": False, "fork": False, "rand": 0.3, "iter": False},
            "medium":  {"depth": 2, "heuristic": 2, "time": 0.6, "block": True,  "win": False, "fork": False, "rand": 0.1, "iter": False},
            "hard":    {"depth": 3, "heuristic": 3, "time": 1.5, "block": True,  "win": True,  "fork": True,  "rand": 0.05,"iter": False},
            "expert":  {"depth": 4, "heuristic": 4, "time": 5.0, "block": True,  "win": True,  "fork": True,  "rand": 0.0, "iter": True},
        }

        cfg = difficulty_config.get(self.difficulty, difficulty_config["easy"])

        # FINAL depth
        self.depth = depth if depth is not None else cfg["depth"]

        # FINAL heuristic mode
        self.mode = mode_from_gui if mode_from_gui is not None else cfg["heuristic"]

        # Other parameters
        self.time_limit = cfg["time"]
        self.enable_blocking = cfg["block"]
        self.enable_winning = cfg["win"]
        self.enable_forking = cfg["fork"]
        self.randomness = cfg["rand"]
        self.use_iterative = cfg["iter"]

    def in_bounds(self, n, r, c):
        return 0 <= r < n and 0 <= c < n

    def find_winning_move(self, board, player):
        n = board.n
        g = board.grid
        for r in range(n):
            for c in range(n):
                if g[r][c] != EMPTY:
                    continue
                g[r][c] = player
                if board.check_winner(player):
                    g[r][c] = EMPTY
                    return (r, c)
                g[r][c] = EMPTY
        return None

    def find_block_move(self, board):
        n = board.n
        g = board.grid
        dirs = [(1,0),(0,1),(1,1),(1,-1)]

        for dr, dc in dirs:
            for r in range(n):
                for c in range(n):
                    cells = []
                    vals = []
                    for i in range(5):
                        rr = r + i*dr
                        cc = c + i*dc
                        if not self.in_bounds(n, rr, cc):
                            break
                        cells.append((rr, cc))
                        vals.append(g[rr][cc])
                    if len(vals) < 5:
                        continue
                    if vals.count(HUMAN) == 4 and vals.count(EMPTY) == 1:
                        return cells[vals.index(EMPTY)]
        return None

    def find_fork_move(self, board, player):
        n = board.n
        g = board.grid
        for r in range(n):
            for c in range(n):
                if g[r][c] != EMPTY:
                    continue
                g[r][c] = player
                threats = 0
                for rr in range(n):
                    for cc in range(n):
                        if g[rr][cc] == EMPTY:
                            g[rr][cc] = player
                            if board.check_winner(player):
                                threats += 1
                            g[rr][cc] = EMPTY
                        if threats >= 2:
                            g[r][c] = EMPTY
                            return (r, c)
                g[r][c] = EMPTY
        return None



    def get_best_move(self, board):
        n = board.n
        g = board.grid

        if all(g[r][c] == EMPTY for r in range(n) for c in range(n)):
            return (n//2, n//2)

        if random.random() < self.randomness:
            empties = [(r,c) for r in range(n) for c in range(n) if g[r][c] == EMPTY]
            return random.choice(empties)

        if self.enable_winning:
            win = self.find_winning_move(board, AI)
            if win:
                return win
            
        if self.enable_blocking:
            block = self.find_winning_move(board, HUMAN)
            if block:
                return block

        if self.enable_forking:
            fork = self.find_fork_move(board, AI)
            if fork:
                return fork
        if self.enable_forking:
            opp_fork = self.find_fork_move(board, HUMAN)
            if opp_fork:
                return opp_fork

        start = time.time()

        if self.use_iterative:
            move = iterative_deepening(board, self.depth, self.mode, time_limit=self.time_limit)
            if move:
                return move

        _, move = minimax(
            board,
            self.depth,
            -1e9, 1e9,
            True,
            self.mode,
            start,
            self.time_limit
        )

        return move
