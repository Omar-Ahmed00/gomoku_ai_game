# ai/ai_player.py
import random
import time
from ai.minimax import minimax, STATS
from ai.heuristics import EMPTY

class AIPlayer:
    def __init__(self, difficulty="medium", board_size=15):
        """
        AI Player that fulfills Project Requirements:
        - Adaptive Difficulty
        - Supports Minimax & Alpha-Beta toggling (for experiments)
        - Supports switching Heuristics (for experiments)
        """
        self.diff = difficulty.lower()
        self.board_size = board_size
        
        # Default Configuration
        self.heuristic_mode = 2  # Default to Advanced (H2)
        self.use_pruning = True  # Default to Alpha-Beta On
        
        # Difficulty Profiles
        # Depth: How many moves ahead to look
        # Rand: Chance to make a random move (simulates human error)
        self.configs = {
            "easy":     {"depth": 1, "rand": 0.6, "limit": 1.0, "pruning": True,  "heuristic": 1}, # Use Simple H1
            "medium":   {"depth": 2, "rand": 0.2, "limit": 2.0, "pruning": True,  "heuristic": 2}, # Use Advanced H2
            "hard":     {"depth": 3, "rand": 0.0, "limit": 4.0, "pruning": True,  "heuristic": 2},
            "adaptive": {"dynamic": True,         "limit": 5.0, "pruning": True,  "heuristic": 2}
        }
        
        self.current_cfg = self.configs[self.diff]

    def adaptive_depth(self, board):
        """
        Requirement: Adaptive Difficulty
        Adjusts depth based on how full the board is.
        """
        n = board.n
        filled = sum(row.count(EMPTY) for row in board.grid)
        total = n * n
        fill_ratio = (total - filled) / total

        if fill_ratio < 0.1: return 1  # Opening (Fast)
        if fill_ratio < 0.3: return 2  # Mid-game
        return 3                       # Late-game (Deep thinking)

    def get_best_move(self, board):
        n = board.n
        
        # Reset Stats for the Report
        STATS["nodes_evaluated"] = 0
        STATS["pruning_count"] = 0
        start_time = time.time()

        # 1. Handle First Move (Center is optimal)
        if board.move_count == 0:
            return (n//2, n//2)

        # 2. Determine Settings
        if self.diff == "adaptive":
            depth = self.adaptive_depth(board)
            rand_chance = 0.1
        else:
            depth = self.current_cfg["depth"]
            rand_chance = self.current_cfg["rand"]

        # 3. Easy Mode Randomness
        if random.random() < rand_chance:
            import ai.minimax as mm
            moves = mm.gen_moves(board)
            if moves: return random.choice(moves)

        # 4. Run Minimax / Alpha-Beta
        # Note: We pass the flags for Heuristic Mode and Pruning here
        score, move = minimax(
            board,
            depth,
            -float('inf'), 
            float('inf'),
            True,  # maximizing player (AI)
            self.current_cfg["heuristic"], # Mode 1 or 2
            start_time,
            self.current_cfg["limit"],
            use_pruning=self.current_cfg["pruning"]
        )

        end_time = time.time()
        duration = end_time - start_time
        
        # --- PRINT STATS FOR YOUR REPORT ---
        print(f"[{self.diff.upper()}] Move: {move}")
        print(f"   Time: {duration:.4f}s")
        print(f"   Nodes: {STATS['nodes_evaluated']}")
        print(f"   Pruned: {STATS['pruning_count']} branches")
        print(f"   Heuristic: H{self.current_cfg['heuristic']}")
        print("-" * 30)

        return move