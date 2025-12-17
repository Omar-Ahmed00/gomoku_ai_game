from game.constants import BLACK, WHITE, EMPTY
from ai.heuristics import Heuristics, DefensiveAI
import time

class Minimax:
    def __init__(self, depth=3):
        self.depth = depth
        self.nodes_explored = 0
        self.start_time = 0
        self.max_time = 10  # seconds
        self.transposition_table = {}  # Cache evaluations
    
    def find_best_move(self, board, player):
        """Find best move - NOW WITH THREAT DETECTION!"""
        self.nodes_explored = 0
        self.start_time = time.time()
        self.transposition_table = {}
        
        # FIRST: Check if we can win immediately
        defensive_move = DefensiveAI.get_defensive_move(board, player)
        if defensive_move:
            print(f"🎯 STRATEGIC MOVE FOUND: {defensive_move}")
            return defensive_move
        
        best_score = float('-inf')
        best_move = None
        
        # Get candidate moves
        candidate_moves = self.get_candidate_moves(board, player)
        
        print(f"🤔 Evaluating {len(candidate_moves)} candidate moves...")
        
        for row, col in candidate_moves:
            if time.time() - self.start_time > self.max_time:
                break
            
            board.board[row][col] = player
            
            # Score this move
            score = self.minimax_alpha_beta(
                board, 
                self.depth - 1, 
                float('-inf'), 
                float('inf'), 
                is_maximizing=False,
                player=player
            )
            
            board.board[row][col] = EMPTY
            
            print(f"  Move ({row}, {col}): score = {score}")
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        if not best_move:
            best_move = self.get_center_move(board)
        
        print(f"✅ BEST MOVE: {best_move} with score {best_score}")
        return best_move
    
    def minimax_alpha_beta(self, board, depth, alpha, beta, is_maximizing, player):
        """Minimax with alpha-beta pruning - IMPROVED"""
        self.nodes_explored += 1
        
        # Terminal conditions
        if depth == 0 or time.time() - self.start_time > self.max_time:
            return Heuristics.evaluate_board(board, player)
        
        # Check for immediate wins/losses
        opponent = BLACK if is_maximizing else WHITE
        
        # Can AI win?
        for row, col in self.get_candidate_moves(board, player)[:5]:
            if board.board[row][col] == EMPTY:
                board.board[row][col] = WHITE if is_maximizing else BLACK
                if board.check_winner(row, col, WHITE if is_maximizing else BLACK):
                    board.board[row][col] = EMPTY
                    return 999999 if is_maximizing else -999999
                board.board[row][col] = EMPTY
        
        if is_maximizing:
            max_eval = float('-inf')
            for row, col in self.get_candidate_moves(board, player)[:10]:
                if board.board[row][col] == EMPTY:
                    board.board[row][col] = WHITE
                    
                    eval_score = self.minimax_alpha_beta(
                        board, depth - 1, alpha, beta, False, player
                    )
                    
                    board.board[row][col] = EMPTY
                    max_eval = max(eval_score, max_eval)
                    alpha = max(alpha, eval_score)
                    
                    if beta <= alpha:
                        break
            
            return max_eval if max_eval != float('-inf') else 0
        else:
            min_eval = float('inf')
            for row, col in self.get_candidate_moves(board, player)[:10]:
                if board.board[row][col] == EMPTY:
                    board.board[row][col] = BLACK
                    
                    eval_score = self.minimax_alpha_beta(
                        board, depth - 1, alpha, beta, True, player
                    )
                    
                    board.board[row][col] = EMPTY
                    min_eval = min(eval_score, min_eval)
                    beta = min(beta, eval_score)
                    
                    if beta <= alpha:
                        break
            
            return min_eval if min_eval != float('inf') else 0
    
    def get_candidate_moves(self, board, player):
        """Get promising moves - INTELLIGENTLY"""
        if not board.move_history:
            center = board.size // 2
            return [(center, center)]
        
        # Get all moves near existing stones (within distance 3)
        candidates = set()
        
        for row, col, _ in board.move_history:
            for dr in range(-3, 4):
                for dc in range(-3, 4):
                    r, c = row + dr, col + dc
                    if 0 <= r < board.size and 0 <= c < board.size:
                        if board.board[r][c] == EMPTY:
                            candidates.add((r, c))
        
        # Score candidates by threat level
        scored_candidates = []
        for row, col in candidates:
            board.board[row][col] = player
            threat_score = Heuristics.evaluate_stone(board, row, col, player)
            board.board[row][col] = EMPTY
            scored_candidates.append(((row, col), threat_score))
        
        # Sort by threat (best first)
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        return [move for move, _ in scored_candidates[:20]]
    
    def get_center_move(self, board):
        center = board.size // 2
        return (center, center)