import tkinter as tk
from tkinter import messagebox, ttk
import threading
from PIL import Image, ImageDraw, ImageTk
from game.board import Board
from game.constants import EMPTY, BLACK, WHITE
from ai.ai_player import AIPlayer

class GomokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Intelligent Gomoku Player")
        self.root.geometry("1000x800")
        self.root.configure(bg="#1e1e1e")
        
        # Game variables
        self.board_size = tk.IntVar(value=15)
        self.difficulty = tk.StringVar(value="Medium")
        self.board = None
        self.ai_player = None
        self.current_player = BLACK
        self.game_active = False
        self.ai_thinking = False
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the entire UI"""
        # Main container
        main_container = tk.Frame(self.root, bg="#1e1e1e")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top control panel
        self.create_control_panel(main_container)
        
        # Middle section (board + info)
        middle_frame = tk.Frame(main_container, bg="#1e1e1e")
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Board canvas
        self.create_board_canvas(middle_frame)
        
        # Right info panel
        self.create_info_panel(middle_frame)
        
        # Bottom status bar
        self.create_status_bar(main_container)
        
    def create_control_panel(self, parent):
        """Create top control panel"""
        control_frame = tk.Frame(parent, bg="#2d2d2d", relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = tk.Label(
            control_frame, 
            text="⚫ GOMOKU AI - Five in a Row ⚪",
            font=("Arial", 16, "bold"),
            bg="#2d2d2d",
            fg="#00ff00"
        )
        title_label.pack(pady=5)
        
        # Settings frame
        settings_frame = tk.Frame(control_frame, bg="#2d2d2d")
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Board size selector
        tk.Label(settings_frame, text="Board Size:", bg="#2d2d2d", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        board_sizes = [9, 13, 15, 19]
        size_combo = ttk.Combobox(settings_frame, textvariable=self.board_size, values=board_sizes, width=5, state="readonly")
        size_combo.pack(side=tk.LEFT, padx=5)
        
        # Difficulty selector
        tk.Label(settings_frame, text="Difficulty:", bg="#2d2d2d", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        difficulty_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.difficulty,
            values=["Easy", "Medium", "Hard", "Expert"],
            width=10,
            state="readonly"
        )
        difficulty_combo.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = tk.Frame(settings_frame, bg="#2d2d2d")
        button_frame.pack(side=tk.RIGHT, padx=10)
        
        start_btn = tk.Button(
            button_frame,
            text="▶ Start Game",
            command=self.start_game,
            bg="#00aa00",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        start_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(
            button_frame,
            text="🔄 Reset",
            command=self.reset_game,
            bg="#aa6600",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        undo_btn = tk.Button(
            button_frame,
            text="↶ Undo",
            command=self.undo_move,
            bg="#0066aa",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        undo_btn.pack(side=tk.LEFT, padx=5)
        
    def create_board_canvas(self, parent):
        """Create the game board canvas"""
        board_frame = tk.Frame(parent, bg="#1e1e1e")
        board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Canvas size
        self.canvas_size = 600
        self.canvas = tk.Canvas(
            board_frame,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#d4a574",
            relief=tk.SUNKEN,
            bd=2
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # PIL Image for drawing
        self.pil_image = Image.new("RGB", (self.canvas_size, self.canvas_size), color="#d4a574")
        self.photo_image = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
        
    def create_info_panel(self, parent):
        """Create right info panel"""
        info_frame = tk.Frame(parent, bg="#2d2d2d", relief=tk.RAISED, bd=2, width=250)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 0))
        info_frame.pack_propagate(False)
        
        # Game status
        tk.Label(info_frame, text="GAME STATUS", bg="#2d2d2d", fg="#00ff00", font=("Arial", 12, "bold")).pack(pady=10)
        
        self.status_label = tk.Label(
            info_frame,
            text="Not Started",
            bg="#2d2d2d",
            fg="#ffff00",
            font=("Arial", 11),
            wraplength=200
        )
        self.status_label.pack(pady=5, padx=10)
        
        # Current turn
        tk.Label(info_frame, text="CURRENT TURN", bg="#2d2d2d", fg="#00ff00", font=("Arial", 12, "bold")).pack(pady=(20, 5))
        
        self.turn_label = tk.Label(
            info_frame,
            text="⚫ Black (You)",
            bg="#2d2d2d",
            fg="white",
            font=("Arial", 11)
        )
        self.turn_label.pack(pady=5)
        
        # Game stats
        tk.Label(info_frame, text="STATISTICS", bg="#2d2d2d", fg="#00ff00", font=("Arial", 12, "bold")).pack(pady=(20, 5))
        
        self.stats_label = tk.Label(
            info_frame,
            text="Moves: 0\nAI Depth: N/A\nThinking Time: 0s",
            bg="#2d2d2d",
            fg="#cccccc",
            font=("Arial", 10),
            justify=tk.LEFT
        )
        self.stats_label.pack(pady=5, padx=10)
        
        # Instructions
        tk.Label(info_frame, text="INSTRUCTIONS", bg="#2d2d2d", fg="#00ff00", font=("Arial", 12, "bold")).pack(pady=(20, 5))
        
        instructions = """
1. Select board size (9-19)
2. Choose difficulty level
3. Click 'Start Game'
4. Click on board to place pieces
5. Get 5 in a row to win!

Your color: ⚫ Black
AI color: ⚪ White
        """
        
        tk.Label(
            info_frame,
            text=instructions,
            bg="#2d2d2d",
            fg="#aaaaaa",
            font=("Arial", 9),
            justify=tk.LEFT
        ).pack(pady=5, padx=10)
        
    def create_status_bar(self, parent):
        """Create bottom status bar"""
        status_frame = tk.Frame(parent, bg="#1a1a1a", relief=tk.SUNKEN, bd=2)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_bar = tk.Label(
            status_frame,
            text="Ready to start a new game",
            bg="#1a1a1a",
            fg="#00aa00",
            font=("Arial", 10)
        )
        self.status_bar.pack(side=tk.LEFT, padx=10, pady=5)
        
    def start_game(self):
        """Initialize and start the game"""
        try:
            size = self.board_size.get()
            difficulty_map = {"Easy": 2, "Medium": 3, "Hard": 5, "Expert": 7}
            depth = difficulty_map[self.difficulty.get()]
            
            # Initialize board and AI
            self.board = Board(size)
            self.ai_player = AIPlayer(WHITE, depth)
            
            self.current_player = BLACK
            self.game_active = True
            
            self.update_status_bar(f"Game started! {size}x{size} board, {self.difficulty.get()} difficulty")
            self.update_turn_label()
            self.draw_board()
            
            messagebox.showinfo("Game Started", 
                f"Game started on {size}x{size} board!\n\nYou are ⚫ Black\nAI is ⚪ White\n\nYou play first!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start game: {str(e)}")
            
    def reset_game(self):
        """Reset the game board"""
        if self.board:
            self.board.reset()
            self.current_player = BLACK
            self.update_turn_label()
            self.draw_board()
            self.update_status_bar("Game reset!")
            
    def undo_move(self):
        """Undo last move"""
        messagebox.showinfo("Undo", "Undo functionality can be implemented by maintaining move history")
        
    def on_canvas_click(self, event):
        """Handle canvas click for player move"""
        if not self.game_active or self.ai_thinking or self.current_player != BLACK:
            return
        
        # Convert pixel coordinates to board coordinates
        row, col = self.pixel_to_board(event.x, event.y)
        
        if row is not None and col is not None:
            if self.board.is_valid_move(row, col):
                # Make player move
                self.board.place_stone(row, col, BLACK)
                self.draw_board()
                self.update_status_bar(f"You played at ({row}, {col})")
                
                # Check for player win
                if self.board.check_winner(row, col, BLACK):
                    self.end_game("🎉 Congratulations! You Won!")
                    return
                
                # AI turn
                self.current_player = WHITE
                self.update_turn_label()
                self.ai_thinking = True
                self.update_status_bar("AI is thinking...")
                
                # Run AI move in separate thread
                threading.Thread(target=self.ai_move, daemon=True).start()
            else:
                messagebox.showwarning("Invalid Move", "That position is already occupied!")
                
    def ai_move(self):
        """Perform AI move in separate thread"""
        try:
            row, col = self.ai_player.get_best_move(self.board)
            
            self.board.place_stone(row, col, WHITE)
            
            # Check for AI win
            if self.board.check_winner(row, col, WHITE):
                self.root.after(0, lambda: self.end_game("😢 AI Won! Game Over!"))
                return
            
            self.current_player = BLACK
            self.root.after(0, self.update_after_ai_move, row, col)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("AI Error", str(e)))
        finally:
            self.ai_thinking = False
            
    def update_after_ai_move(self, row, col):
        """Update UI after AI move"""
        import time
        elapsed_time = time.time() - self.ai_player.minimax.start_time
        move_count = len(self.board.move_history)
        ai_depth = self.ai_player.depth
        
        self.draw_board()
        self.update_turn_label()
        
        self.stats_label.config(
            text=f"Moves: {move_count}\nAI Depth: {ai_depth}\nThinking Time: ~{elapsed_time:.2f}s"
        )
        
        self.update_status_bar(f"AI played at ({row}, {col})")
        
    def end_game(self, message):
        """End the game"""
        self.game_active = False
        messagebox.showinfo("Game Over", message)
        self.update_status_bar("Game Over! Click 'Start Game' to play again")
        
    def draw_board(self):
        """Draw the game board"""
        draw = ImageDraw.Draw(self.pil_image)
        
        # Background
        draw.rectangle([0, 0, self.canvas_size, self.canvas_size], fill="#d4a574")
        
        if not self.board:
            self.photo_image = ImageTk.PhotoImage(self.pil_image)
            self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
            return
        
        # Calculate grid
        size = self.board.size
        cell_size = self.canvas_size // (size + 1)
        offset = cell_size
        
        # Draw grid lines
        line_color = "#000000"
        for i in range(size):
            # Horizontal
            y = offset + i * cell_size
            draw.line([(offset, y), (self.canvas_size - offset, y)], fill=line_color, width=1)
            # Vertical
            x = offset + i * cell_size
            draw.line([(x, offset), (x, self.canvas_size - offset)], fill=line_color, width=1)
        
        # Draw stones
        for row in range(size):
            for col in range(size):
                x = offset + col * cell_size
                y = offset + row * cell_size
                
                if self.board.board[row][col] == BLACK:
                    draw.ellipse([x-8, y-8, x+8, y+8], fill="#000000")
                elif self.board.board[row][col] == WHITE:
                    draw.ellipse([x-8, y-8, x+8, y+8], fill="#ffffff", outline="#000000", width=1)
        
        self.photo_image = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
        
    def pixel_to_board(self, px, py):
        """Convert pixel coordinates to board coordinates"""
        if not self.board:
            return None, None
        
        size = self.board.size
        cell_size = self.canvas_size // (size + 1)
        offset = cell_size
        
        col = round((px - offset) / cell_size)
        row = round((py - offset) / cell_size)
        
        if 0 <= row < size and 0 <= col < size:
            return row, col
        return None, None
        
    def update_turn_label(self):
        """Update current turn label"""
        if self.current_player == BLACK:
            self.turn_label.config(text="⚫ Black (You)", fg="#ffff00")
        else:
            self.turn_label.config(text="⚪ White (AI)", fg="#ffffff")
            
    def update_status_bar(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        
def run_gui():
    """Run the GUI"""
    root = tk.Tk()
    gui = GomokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()