from game.constants import WHITE, BLACK, EMPTY
from ai.heuristics import Heuristics
import time

class AIPlayer:
    def __init__(self, player_color, difficulty="Medium"):
        self.color = player_color
        self.difficulty = difficulty
        
        # Set depth based on difficulty
        self.depth_map = {
            "Easy": 2,
            "Medium": 3,
            "Hard": 5,
            "Expert": 6
        }
        
        self.depth = self.depth_map.get(difficulty, 3)
        print(f"🤖 AI Player initialized: {difficulty} (depth={self.depth})")
    
    def get_best_move(self, board):
        """Get best move - PRIORITY SYSTEM"""
        print(f"\n{'='*60}")
        print(f"🤖 AI PLAYING ({self.difficulty} - Depth {self.depth})")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # PRIORITY 1: Can we WIN this turn?
        win_move = Heuristics.find_immediate_win(board, self.color)
        if win_move:
            elapsed = time.time() - start_time
            print(f"✅ PRIORITY 1: AI CAN WIN! Playing: {win_move}")
            print(f"⏱️  Time: {elapsed:.2f}s\n")
            return win_move
        
        # PRIORITY 2: Must we BLOCK opponent?
        block_move = Heuristics.find_threat_to_block(board, BLACK if self.color == WHITE else WHITE)
        if block_move:
            elapsed = time.time() - start_time
            print(f"🛡️  PRIORITY 2: BLOCKING THREAT at {block_move}")
            print(f"⏱️  Time: {elapsed:.2f}s\n")
            return block_move
        
        # PRIORITY 3: Smart strategic move
        best_move = self.find_best_strategic_move(board)
        elapsed = time.time() - start_time
        print(f"🎯 PRIORITY 3: Strategic move: {best_move}")
        print(f"⏱️  Time: {elapsed:.2f}s")
        print(f"{'='*60}\n")
        
        return best_move
    
    def find_best_strategic_move(self, board):
        """Find best move using minimax"""
        candidates = self.get_candidate_moves(board)
        
        best_score = float('-inf')
        best_move = candidates[0] if candidates else (board.size // 2, board.size // 2)
        
        print(f"📊 Evaluating {len(candidates)} moves...")
        
        for row, col in candidates:
            score = Heuristics.evaluate_move(board, row, col, self.color)
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move
    
    def get_candidate_moves(self, board):
        """Get promising positions - near existing stones"""
        if not board.move_history:
            # First move - center
            center = board.size // 2
            return [(center, center)]
        
        candidates = set()
        
        # Add positions near all existing stones
        for row, col, _ in board.move_history:
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    r, c = row + dr, col + dc
                    if 0 <= r < board.size and 0 <= c < board.size:
                        if board.board[r][c] == EMPTY:
                            candidates.add((r, c))
        
        # Score and sort candidates
        scored = []
        for row, col in candidates:
            score = Heuristics.evaluate_move(board, row, col, self.color)
            scored.append(((row, col), score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Return top candidates only
        return [move for move, _ in scored[:15]]