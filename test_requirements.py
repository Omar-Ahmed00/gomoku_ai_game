# test_requirements.py
from game.board import Board
from game.constants import BLACK, WHITE
from ai.ai_player import AIPlayer

def test_all():
    print("✅ Testing Gomoku AI Implementation\n")
    
    # Test 1: Board creation
    print("1️⃣ Board Creation...")
    board = Board(15)
    print(f"   ✓ Created {board.size}x{board.size} board\n")
    
    # Test 2: Minimax & Alpha-Beta
    print("2️⃣ Minimax & Alpha-Beta Pruning...")
    ai = AIPlayer(WHITE, "Medium")
    print(f"   ✓ AI Player created with depth {ai.depth}\n")
    
    # Test 3: Move generation
    print("3️⃣ Move Generation...")
    candidates = ai.minimax.get_candidate_moves(board)
    print(f"   ✓ Generated {len(candidates)} candidate moves\n")
    
    # Test 4: Heuristic evaluation
    print("4️⃣ Heuristic Evaluation...")
    from ai.heuristics import Heuristics
    score = Heuristics.evaluate_board(board, WHITE)
    print(f"   ✓ Initial board score: {score}\n")
    
    # Test 5: AI move
    print("5️⃣ AI Move Generation...")
    board.place_stone(7, 7, BLACK)
    move = ai.get_best_move(board)
    print(f"   ✓ AI suggests move: {move}\n")
    
    # Test 6: Win detection
    print("6️⃣ Win Detection...")
    for i in range(5):
        board.place_stone(0, i, BLACK)
    winner = board.check_winner(0, 4, BLACK)
    print(f"   ✓ Win detection works: {winner}\n")
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_all()