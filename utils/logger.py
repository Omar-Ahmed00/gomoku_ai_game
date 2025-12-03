"""
Logging utilities for Gomoku AI project
Author: [Your Name/Team]
"""

import logging
import time
from datetime import datetime

class GameLogger:
    def __init__(self, log_file="gomoku_game.log"):
        """
        Initialize game logger
        
        Args:
            log_file: Path to log file
        """
        self.log_file = log_file
        self.setup_logger()
    
    def setup_logger(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_game_start(self, board_size, difficulty, mode):
        """Log game start"""
        self.logger.info(f"Game Started - Board: {board_size}x{board_size}, "
                        f"Difficulty: {difficulty}, Mode: {mode}")
    
    def log_move(self, player, row, col, move_time=None):
        """Log a move"""
        if move_time:
            self.logger.info(f"{player} moved to ({row}, {col}) in {move_time:.2f}s")
        else:
            self.logger.info(f"{player} moved to ({row}, {col})")
    
    def log_game_end(self, winner, total_moves, duration):
        """Log game end"""
        if winner:
            self.logger.info(f"Game Ended - Winner: {winner}, "
                           f"Moves: {total_moves}, Duration: {duration:.2f}s")
        else:
            self.logger.info(f"Game Ended - Draw, "
                           f"Moves: {total_moves}, Duration: {duration:.2f}s")
    
    def log_ai_thinking(self, depth, nodes_evaluated, search_time):
        """Log AI thinking process"""
        self.logger.debug(f"AI Search - Depth: {depth}, "
                         f"Nodes: {nodes_evaluated}, Time: {search_time:.2f}s")
    
    def log_error(self, error_message):
        """Log an error"""
        self.logger.error(f"Error: {error_message}")
    
    def log_stats(self, stats):
        """Log game statistics"""
        self.logger.info(f"Statistics - {stats}")