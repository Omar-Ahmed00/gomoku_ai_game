from game.constants import EMPTY, BLACK, WHITE, WIN_LENGTH

class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = [[EMPTY] * size for _ in range(size)]
        self.move_history = []
        
    def is_valid_move(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col] == EMPTY
        return False
    
    def place_stone(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            self.move_history.append((row, col, player))
            return True
        return False
    
    def check_winner(self, row, col, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            # Check positive direction
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            
            # Check negative direction
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            
            if count >= WIN_LENGTH:
                return True
        
        return False
    
    def reset(self):
        self.board = [[EMPTY] * self.size for _ in range(self.size)]
        self.move_history = []
    
    def get_empty_positions(self):
        positions = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == EMPTY:
                    positions.append((row, col))
        return positions