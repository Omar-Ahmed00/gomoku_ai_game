from game.constants import BLACK, WHITE, EMPTY

class Heuristics:
    @staticmethod
    def find_immediate_win(board, player):
        """Check if player can WIN THIS TURN - SIMPLE & DIRECT"""
        for row in range(board.size):
            for col in range(board.size):
                if board.board[row][col] == EMPTY:
                    # Try placing stone here
                    board.board[row][col] = player
                    
                    # Check if this wins
                    if board.check_winner(row, col, player):
                        board.board[row][col] = EMPTY
                        return (row, col)  # WIN FOUND!
                    
                    board.board[row][col] = EMPTY
        
        return None
    
    @staticmethod
    def find_threat_to_block(board, opponent):
        """Check if opponent can WIN NEXT TURN - BLOCK IT!"""
        for row in range(board.size):
            for col in range(board.size):
                if board.board[row][col] == EMPTY:
                    # Try opponent placing stone here
                    board.board[row][col] = opponent
                    
                    # Check if opponent wins
                    if board.check_winner(row, col, opponent):
                        board.board[row][col] = EMPTY
                        return (row, col)  # THREAT FOUND - BLOCK HERE!
                    
                    board.board[row][col] = EMPTY
        
        return None
    
    @staticmethod
    def count_in_line(board, row, col, player, dr, dc):
        """Count stones in one direction"""
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < board.size and 0 <= c < board.size:
            if board.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            else:
                break
        return count
    
    @staticmethod
    def evaluate_move(board, row, col, player):
        """Score a move - SIMPLE EVALUATION"""
        score = 0
        
        # Try the move
        board.board[row][col] = player
        
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            # Count in both directions
            forward = Heuristics.count_in_line(board, row, col, player, dr, dc)
            backward = Heuristics.count_in_line(board, row, col, player, -dr, -dc)
            
            total = forward + backward + 1
            
            # Score based on line length
            if total >= 5:
                score += 1000000  # WIN!
            elif total == 4:
                score += 100000   # Close to winning
            elif total == 3:
                score += 10000    # Three in a row
            elif total == 2:
                score += 1000     # Two in a row
            elif total == 1:
                score += 100      # Single stone
        
        board.board[row][col] = EMPTY
        return score