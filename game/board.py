"""
Board class for Gomoku game with enhanced features
Author: [Your Name/Team]
"""

EMPTY = 0
AI = 1
HUMAN = -1

class Board:
    def __init__(self, n=15):
        """
        Initialize Gomoku board
        
        Args:
            n: board size (n x n)
        """
        self.n = n
        self.grid = [[EMPTY for _ in range(n)] for _ in range(n)]
        self.move_history = []  # Track moves for undo/redo
        self.current_player = HUMAN  # Human starts first
        
        # Pre-calculate directions for winner checking
        self.directions = [
            (1, 0),   # vertical
            (0, 1),   # horizontal
            (1, 1),   # diagonal \
            (1, -1)   # diagonal /
        ]
        
        # Statistics
        self.move_count = 0
        self.last_move = None
    
    def make_move(self, r, c, player):
        """
        Place a piece on the board
        
        Args:
            r: row (0-indexed)
            c: column (0-indexed)
            player: AI (1) or HUMAN (-1)
        
        Returns:
            bool: True if move was valid and made
        """
        if not self.is_valid_move(r, c):
            return False
        
        self.grid[r][c] = player
        self.move_history.append((r, c, player))
        self.move_count += 1
        self.last_move = (r, c)
        self.current_player = -player  # Switch player
        
        return True
    
    def undo_move(self, r=None, c=None):
        """
        Undo the last move
        
        Args:
            r, c: specific position to undo (optional)
        
        Returns:
            bool: True if undo was successful
        """
        if not self.move_history:
            return False
        
        if r is not None and c is not None:
            # Undo specific move
            for i in range(len(self.move_history)-1, -1, -1):
                mr, mc, mp = self.move_history[i]
                if mr == r and mc == c:
                    self.grid[mr][mc] = EMPTY
                    del self.move_history[i]
                    self.move_count -= 1
                    self.current_player = mp  # Switch back to this player
                    
                    # Update last move
                    if self.move_history:
                        self.last_move = self.move_history[-1][:2]
                    else:
                        self.last_move = None
                    return True
            return False
        else:
            # Undo last move
            r, c, player = self.move_history.pop()
            self.grid[r][c] = EMPTY
            self.move_count -= 1
            self.current_player = player
            
            # Update last move
            if self.move_history:
                self.last_move = self.move_history[-1][:2]
            else:
                self.last_move = None
            
            return True
    
    def is_valid_move(self, r, c):
        """Check if move is within board and on empty cell"""
        return (0 <= r < self.n and 0 <= c < self.n and 
                self.grid[r][c] == EMPTY)
    
    def check_winner(self, player):
        """
        Check if specified player has won
        
        Args:
            player: AI (1) or HUMAN (-1)
        
        Returns:
            bool: True if player has won
        """
        g = self.grid
        
        for r in range(self.n):
            for c in range(self.n):
                if g[r][c] != player:
                    continue
                
                for dr, dc in self.directions:
                    count = 1
                    
                    # Check forward direction
                    nr, nc = r + dr, c + dc
                    while (0 <= nr < self.n and 0 <= nc < self.n and 
                           g[nr][nc] == player):
                        count += 1
                        nr += dr
                        nc += dc
                    
                    # Check backward direction
                    nr, nc = r - dr, c - dc
                    while (0 <= nr < self.n and 0 <= nc < self.n and 
                           g[nr][nc] == player):
                        count += 1
                        nr -= dr
                        nc -= dc
                    
                    if count >= 5:
                        return True
        
        return False
    
    def get_winner(self):
        """Check if there's a winner and return which player"""
        if self.check_winner(AI):
            return AI
        if self.check_winner(HUMAN):
            return HUMAN
        return None
    
    def is_game_over(self):
        """Check if game is over (win or draw)"""
        if self.get_winner() is not None:
            return True
        
        # Check for draw (board full)
        return all(cell != EMPTY for row in self.grid for cell in row)
    
    def get_moves(self):
        """
        Get all possible moves
        
        Returns:
            list: [(row, col), ...] of empty cells
        """
        # If there are existing pieces, only consider adjacent moves
        # for better performance (Gomoku is usually played locally)
        moves = []
        
        if self.move_count == 0:
            # First move: center or nearby
            center = self.n // 2
            for r in range(center-1, center+2):
                for c in range(center-1, center+2):
                    if self.is_valid_move(r, c):
                        moves.append((r, c))
            return moves
        
        # Get moves adjacent to existing pieces
        visited = set()
        for r in range(self.n):
            for c in range(self.n):
                if self.grid[r][c] == EMPTY:
                    continue
                
                # Check all adjacent positions
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < self.n and 0 <= nc < self.n and
                            self.grid[nr][nc] == EMPTY and
                            (nr, nc) not in visited):
                            moves.append((nr, nc))
                            visited.add((nr, nc))
        
        # If no adjacent moves (shouldn't happen), fall back to all moves
        if not moves:
            moves = [(r, c) for r in range(self.n) for c in range(self.n)
                    if self.grid[r][c] == EMPTY]
        
        return moves
    
    def get_board_state(self):
        """Return string representation of board"""
        chars = {EMPTY: '.', AI: 'X', HUMAN: 'O'}
        lines = []
        lines.append('   ' + ' '.join(str(i%10) for i in range(self.n)))
        for r in range(self.n):
            line = f"{r:2d} "
            for c in range(self.n):
                line += chars[self.grid[r][c]] + ' '
            lines.append(line)
        return '\n'.join(lines)
    
    def reset(self):
        """Reset the board to initial state"""
        self.grid = [[EMPTY for _ in range(self.n)] for _ in range(self.n)]
        self.move_history = []
        self.move_count = 0
        self.current_player = HUMAN
        self.last_move = None
    
    def copy(self):
        """Create a deep copy of the board"""
        new_board = Board(self.n)
        new_board.grid = [row[:] for row in self.grid]
        new_board.move_history = self.move_history[:]
        new_board.move_count = self.move_count
        new_board.current_player = self.current_player
        new_board.last_move = self.last_move
        return new_board
    
    def get_score_estimate(self, player):
        """
        Quick score estimate for move ordering
        Simple count of pieces with center bonus
        """
        score = 0
        center = self.n // 2
        
        for r in range(self.n):
            for c in range(self.n):
                if self.grid[r][c] == player:
                    # Base value
                    score += 10
                    # Center control bonus
                    distance = abs(r - center) + abs(c - center)
                    score += max(0, 5 - distance)
        
        return score