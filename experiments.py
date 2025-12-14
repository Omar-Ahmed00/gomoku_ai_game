import time
import statistics
from game.board import Board
from ai.ai_player import AIPlayer
from ai.minimax import STATS
import random  
GAMES_PER_TEST = 3 

def play_game(ai_mode, board_size=9):  
    board = Board(board_size)
    ai = AIPlayer(difficulty=ai_mode, board_size=board_size)

    move_times = []
    nodes = []
    pruned = []

    while not board.is_game_over():
        STATS["nodes_evaluated"] = 0
        STATS["pruning_count"] = 0
        
        start = time.time()
        move = ai.get_best_move(board)
        
        if not move: 
            break
            
        duration = time.time() - start

        move_times.append(duration)
        nodes.append(STATS["nodes_evaluated"])
        pruned.append(STATS["pruning_count"])

        board.make_move(move[0], move[1], 1)

        if board.check_winner(1):
            return True, move_times, nodes, pruned
        empty_cells = []
        for r in range(board.n):
            for c in range(board.n):
                if board.grid[r][c] == 0:
                    empty_cells.append((r, c))
        
        if empty_cells:
            r, c = random.choice(empty_cells)
            board.make_move(r, c, -1)
        else:
            break  

    return False, move_times, nodes, pruned

def run_heuristic_comparison():
    results = {}
    for mode in ["h1_only", "h2_only"]:
        wins = 0
        times, all_nodes, all_pruned = [], [], []

        for game_num in range(GAMES_PER_TEST):
            print(f"\n Testing {mode} - Game {game_num+1}/{GAMES_PER_TEST}")
            win, t, n, p = play_game(mode, board_size=9)  
            
            if win:
                wins += 1
                print(f"  AI won in {len(t)} moves")
            else:
                print(f"   AI didn't win")
                
            times.extend(t)
            all_nodes.extend(n)
            all_pruned.extend(p)

        results[mode] = {
            "win_rate": wins / GAMES_PER_TEST * 100,
            "avg_time": statistics.mean(times) if times else 0,
            "avg_nodes": statistics.mean(all_nodes) if all_nodes else 0,
            "avg_pruning": statistics.mean(all_pruned) if all_pruned else 0,
            "total_moves": len(times)
        }

    return results
def run_pruning_comparison():
    results = {}
    for mode in ["minimax_only", "alpha_beta_only"]:
        wins = 0
        times, all_nodes = [], []

        for game_num in range(GAMES_PER_TEST):
            print(f"\n🎮 Testing {mode} - Game {game_num+1}/{GAMES_PER_TEST}")
            win, t, n, _ = play_game(mode, board_size=9) 
            if win:
                wins += 1
                print(f"  AI won in {len(t)} moves")
            else:
                print(f"  AI didn't win")
                
            times.extend(t)
            all_nodes.extend(n)

        results[mode] = {
            "win_rate": wins / GAMES_PER_TEST * 100,
            "avg_time": statistics.mean(times) if times else 0,
            "avg_nodes": statistics.mean(all_nodes) if all_nodes else 0,
            "total_moves": len(times)
        }

    return results
def run_complete_analysis():
    print("=" * 60)
    print(" COMPLETE AI ALGORITHM ANALYSIS")
    print("=" * 60)
    
    print("\n PRUNING COMPARISON (Minimax vs Alpha-Beta)")
    print("-" * 40)
    pruning_results = run_pruning_comparison()
    
    print("\n PRUNING RESULTS SUMMARY:")
    for mode, data in pruning_results.items():
        print(f"\n{mode.upper()}:")
        print(f"  Win Rate: {data['win_rate']:.1f}%")
        print(f"  Avg Move Time: {data['avg_time']:.4f}s")
        print(f"  Avg Nodes Evaluated: {data['avg_nodes']:.0f}")
        print(f"  Total Moves Analyzed: {data['total_moves']}")
    
    print("\n\n HEURISTIC COMPARISON (H1 vs H2)")
    print("-" * 40)
    heuristic_results = run_heuristic_comparison()
    
    print("\n HEURISTIC RESULTS SUMMARY:")
    for mode, data in heuristic_results.items():
        print(f"\n{mode.upper()}:")
        print(f"  Win Rate: {data['win_rate']:.1f}%")
        print(f"  Avg Move Time: {data['avg_time']:.4f}s")
        print(f"  Avg Nodes Evaluated: {data['avg_nodes']:.0f}")
        print(f"  Avg Pruning Count: {data['avg_pruning']:.0f}")
        print(f"  Total Moves Analyzed: {data['total_moves']}")
    if "minimax_only" in pruning_results and "alpha_beta_only" in pruning_results:
        mm_time = pruning_results["minimax_only"]["avg_time"]
        ab_time = pruning_results["alpha_beta_only"]["avg_time"]
        mm_nodes = pruning_results["minimax_only"]["avg_nodes"]
        ab_nodes = pruning_results["alpha_beta_only"]["avg_nodes"]
        
        print("\n\n PERFORMANCE IMPROVEMENT ANALYSIS:")
        print("-" * 40)
        print(f"Speed Improvement: {(mm_time/ab_time):.1f}x faster")
        print(f"Nodes Reduction: {(mm_nodes/ab_nodes):.1f}x fewer nodes")
        print(f"Time per Node: {mm_time/mm_nodes:.6f}s vs {ab_time/ab_nodes:.6f}s")
    
    return {
        "pruning": pruning_results,
        "heuristic": heuristic_results
    }


if __name__ == "__main__":
    
    print(" Starting AI Algorithm Experiments...")
    print("Board Size: 9x9 (for faster testing)")
    print(f"Games per test: {GAMES_PER_TEST}")
    print("=" * 60)
    
    all_results = run_complete_analysis()
    
    print("\n" + "=" * 60)
    print("EXPERIMENTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)