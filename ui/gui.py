"""
Modern Gomoku GUI - Cleaned Version
Removed hint features and heuristic controls
Added Adaptive difficulty level
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
from game.board import Board, AI, HUMAN
from ai.ai_player import AIPlayer

# Constants
CELL_SIZE = 35
PADDING = 50

# Dark theme colors
THEME = {
    "name": "Dark Mode",
    "bg": "#1A1A2E",
    "fg": "#E6E6E6",
    "accent": "#4ECDC4",
    "border": "#2D3047",
    "board_bg": "#162447",
    "grid_color": "#3D5A80",
    "human_color": "#FF6B6B",
    "ai_color": "#4ECDC4",
    "highlight": "#FFD166",
    "entry_bg": "#2D3047",
    "entry_fg": "#FFFFFF"
}

class ModernGomokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Intelligent Gomoku AI")
        
        # Set window properties
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # Game state
        self.board = None
        self.ai_player = None
        self.game_active = False
        self.game_mode = "human_vs_ai"
        self.ai_thinking = False
        
        # Statistics
        self.stats = {
            "games": 0,
            "human_wins": 0,
            "ai_wins": 0,
            "draws": 0,
            "total_moves": 0
        }
        
        # Initialize UI
        self.setup_styles()
        self.create_main_layout()
        self.setup_shortcuts()
        
        print("🎮 Gomoku AI Game Started!")
    
    def setup_styles(self):
        """Setup ttk styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
    
    def create_main_layout(self):
        """Create the complete main layout"""
        # Configure root grid
        self.root.configure(bg=THEME["bg"])
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # ========== LEFT SIDEBAR ==========
        self.left_frame = tk.Frame(self.root, bg=THEME["bg"], width=280)
        self.left_frame.grid(row=0, column=0, sticky="ns", padx=(20, 10), pady=20)
        self.left_frame.grid_propagate(False)
        self.create_left_sidebar()
        
        # ========== CENTER BOARD ==========
        self.center_frame = tk.Frame(self.root, bg=THEME["bg"])
        self.center_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)
        self.center_frame.grid_rowconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(0, weight=1)
        
        # Board container with border
        self.board_container = tk.Frame(self.center_frame, bg=THEME["border"])
        self.board_container.grid(row=0, column=0, sticky="nsew")
        
        # Canvas for game board
        self.canvas = tk.Canvas(self.board_container,
                               bg=THEME["board_bg"],
                               highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<Button-1>", self.handle_click)
        
        # Status bar
        self.status_bar = tk.Frame(self.center_frame, bg=THEME["bg"], height=40)
        self.status_bar.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        
        self.status_label = tk.Label(self.status_bar,
                                    text="Ready to play! Click 'New Game' to start.",
                                    font=("Segoe UI", 10),
                                    bg=THEME["bg"],
                                    fg=THEME["fg"])
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # AI thinking indicator
        self.thinking_label = tk.Label(self.status_bar,
                                      text="",
                                      font=("Segoe UI", 9),
                                      bg=THEME["bg"],
                                      fg=THEME["accent"])
        self.thinking_label.pack(side="right", padx=10, pady=5)
        
        # ========== RIGHT SIDEBAR ==========
        self.right_frame = tk.Frame(self.root, bg=THEME["bg"], width=280)
        self.right_frame.grid(row=0, column=2, sticky="ns", padx=(10, 20), pady=20)
        self.right_frame.grid_propagate(False)
        self.create_right_sidebar()
    
    def create_left_sidebar(self):
        """Create left sidebar content"""
        # Title
        title_frame = tk.Frame(self.left_frame, bg=THEME["bg"])
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(title_frame,
                text="🎮 GOMOKU AI",
                font=("Segoe UI", 20, "bold"),
                bg=THEME["bg"],
                fg=THEME["accent"]).pack()
        
        tk.Label(title_frame,
                text="Five in a Row Challenge",
                font=("Segoe UI", 10),
                bg=THEME["bg"],
                fg=THEME["fg"]).pack()
        
        # Divider
        tk.Frame(self.left_frame, height=2, bg=THEME["accent"]).pack(fill="x", pady=10)
        
        # Game Settings
        self.create_settings_section()
        
        # Divider
        tk.Frame(self.left_frame, height=1, bg=THEME["border"]).pack(fill="x", pady=10)
        
        # Game Controls
        self.create_controls_section()
        
        # Divider
        tk.Frame(self.left_frame, height=1, bg=THEME["border"]).pack(fill="x", pady=10)
        
        # Footer
        tk.Label(self.left_frame,
                text="Dark Mode",
                font=("Segoe UI", 9, "italic"),
                bg=THEME["bg"],
                fg=THEME["fg"]).pack(pady=(10, 0))
    
    def create_settings_section(self):
        """Create game settings section"""
        settings_frame = tk.LabelFrame(self.left_frame,
                                      text="⚙️ GAME SETTINGS",
                                      font=("Segoe UI", 12, "bold"),
                                      bg=THEME["bg"],
                                      fg=THEME["accent"],
                                      relief="flat")
        settings_frame.pack(fill="x", padx=5, pady=5)
        
        # Board Size
        tk.Label(settings_frame,
                text="Board Size:",
                font=("Segoe UI", 10),
                bg=THEME["bg"],
                fg=THEME["fg"]).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.size_var = tk.StringVar(value="15")
        self.size_combo = ttk.Combobox(settings_frame,
                                      textvariable=self.size_var,
                                      values=["9", "11", "13", "15", "17", "19"],
                                      width=20,
                                      state="readonly")
        self.size_combo.pack(fill="x", padx=10, pady=(0, 10))
        
        # Difficulty
        tk.Label(settings_frame,
                text="Difficulty:",
                font=("Segoe UI", 10),
                bg=THEME["bg"],
                fg=THEME["fg"]).pack(anchor="w", padx=10, pady=5)
        
        self.diff_var = tk.StringVar(value="Medium")
        self.diff_combo = ttk.Combobox(settings_frame,
                                      textvariable=self.diff_var,
                                      values=["Easy", "Medium", "Hard", "Adaptive"],
                                      width=20,
                                      state="readonly")
        self.diff_combo.pack(fill="x", padx=10, pady=(0, 10))
        
        # First Player
        tk.Label(settings_frame,
                text="First Player:",
                font=("Segoe UI", 10),
                bg=THEME["bg"],
                fg=THEME["fg"]).pack(anchor="w", padx=10, pady=5)
        
        self.player_var = tk.StringVar(value="Human")
        self.player_combo = ttk.Combobox(settings_frame,
                                        textvariable=self.player_var,
                                        values=["Human", "AI"],
                                        width=20,
                                        state="readonly")
        self.player_combo.pack(fill="x", padx=10, pady=(0, 10))
        
    def create_controls_section(self):
        """Create game controls section"""
        controls_frame = tk.LabelFrame(self.left_frame,
                                      text="🎮 GAME CONTROLS",
                                      font=("Segoe UI", 12, "bold"),
                                      bg=THEME["bg"],
                                      fg=THEME["accent"],
                                      relief="flat")
        controls_frame.pack(fill="x", padx=5, pady=5)
        
        # Control buttons
        buttons = [
            ("🆕 New Game", self.start_game, "#4ECDC4"),
            ("↩️ Undo Move", self.undo_move, "#45B7D1"),
            ("🔄 Restart Game", self.restart_game, "#FECA57"),
            ("❓ How to Play", self.show_help, "#FF9FF3")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(controls_frame,
                          text=text,
                          command=command,
                          font=("Segoe UI", 10, "bold"),
                          bg=color,
                          fg="white",
                          activebackground=self.lighten_color(color, 1.2),
                          activeforeground="white",
                          relief="flat",
                          padx=20,
                          pady=10,
                          cursor="hand2")
            btn.pack(fill="x", padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.lighten_color(b.cget("bg"), 1.1)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))
    
    def create_right_sidebar(self):
        """Create right sidebar content"""
        # Game Info
        self.create_game_info_section()
        
        # Divider
        tk.Frame(self.right_frame, height=2, bg=THEME["accent"]).pack(fill="x", pady=10)
        
        # Move History
        self.create_history_section()
        
        # Divider
        tk.Frame(self.right_frame, height=1, bg=THEME["border"]).pack(fill="x", pady=10)
        
        # Statistics
        self.create_stats_section()
    
    def create_game_info_section(self):
        """Create game information section"""
        info_frame = tk.LabelFrame(self.right_frame,
                                  text="📊 GAME INFO",
                                  font=("Segoe UI", 12, "bold"),
                                  bg=THEME["bg"],
                                  fg=THEME["accent"],
                                  relief="flat")
        info_frame.pack(fill="x", padx=5, pady=5)
        
        info_content = tk.Frame(info_frame, bg=THEME["bg"])
        info_content.pack(fill="x", padx=10, pady=10)
        
        # Current Player
        self.player_info = tk.Label(info_content,
                                   text="Current Player: -",
                                   font=("Segoe UI", 10),
                                   bg=THEME["bg"],
                                   fg=THEME["fg"])
        self.player_info.pack(anchor="w", pady=5)
        
        # Move Count
        self.move_count_info = tk.Label(info_content,
                                       text="Moves: 0",
                                       font=("Segoe UI", 10),
                                       bg=THEME["bg"],
                                       fg=THEME["fg"])
        self.move_count_info.pack(anchor="w", pady=5)
        
        # Game Status
        self.game_status_info = tk.Label(info_content,
                                        text="Status: Not Started",
                                        font=("Segoe UI", 10),
                                        bg=THEME["bg"],
                                        fg=THEME["fg"])
        self.game_status_info.pack(anchor="w", pady=5)
        
        # Board Size Info
        self.board_info = tk.Label(info_content,
                                  text="Board: 15×15",
                                  font=("Segoe UI", 10),
                                  bg=THEME["bg"],
                                  fg=THEME["fg"])
        self.board_info.pack(anchor="w", pady=5)
        
        # Difficulty Info
        self.diff_info = tk.Label(info_content,
                                 text="Difficulty: -",
                                 font=("Segoe UI", 10),
                                 bg=THEME["bg"],
                                 fg=THEME["fg"])
        self.diff_info.pack(anchor="w", pady=5)
        
        # Divider
        tk.Frame(info_content, height=1, bg=THEME["border"]).pack(fill="x", pady=10)
        
        # Legend
        tk.Label(info_content,
                text="🎯 LEGEND:",
                font=("Segoe UI", 10, "bold"),
                bg=THEME["bg"],
                fg=THEME["accent"]).pack(anchor="w", pady=(0, 5))
        
        # Human piece
        human_frame = tk.Frame(info_content, bg=THEME["bg"])
        human_frame.pack(anchor="w", pady=2)
        canvas_human = tk.Canvas(human_frame, width=20, height=20, 
                                bg=THEME["bg"], highlightthickness=0)
        canvas_human.pack(side="left")
        canvas_human.create_oval(2, 2, 18, 18, fill=THEME["human_color"], outline="")
        tk.Label(human_frame,
                text=" = Human",
                font=("Segoe UI", 9),
                bg=THEME["bg"],
                fg=THEME["fg"]).pack(side="left", padx=5)
        
        # AI piece
        ai_frame = tk.Frame(info_content, bg=THEME["bg"])
        ai_frame.pack(anchor="w", pady=2)
        canvas_ai = tk.Canvas(ai_frame, width=20, height=20, 
                             bg=THEME["bg"], highlightthickness=0)
        canvas_ai.pack(side="left")
        canvas_ai.create_oval(2, 2, 18, 18, fill=THEME["ai_color"], outline="")
        tk.Label(ai_frame,
                text=" = AI",
                font=("Segoe UI", 9),
                bg=THEME["bg"],
                fg=THEME["fg"]).pack(side="left", padx=5)
    
    def create_history_section(self):
        """Create move history section"""
        history_frame = tk.LabelFrame(self.right_frame,
                                     text="📝 MOVE HISTORY",
                                     font=("Segoe UI", 12, "bold"),
                                     bg=THEME["bg"],
                                     fg=THEME["accent"],
                                     relief="flat")
        history_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # History listbox with scrollbar
        list_frame = tk.Frame(history_frame, bg=THEME["bg"])
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox
        self.history_listbox = tk.Listbox(list_frame,
                                         bg=THEME["entry_bg"],
                                         fg=THEME["entry_fg"],
                                         font=("Consolas", 9),
                                         yscrollcommand=scrollbar.set,
                                         selectbackground=THEME["accent"],
                                         selectforeground="white",
                                         relief="flat",
                                         bd=0,
                                         height=12)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=self.history_listbox.yview)
        
        # Clear button
        clear_btn = tk.Button(history_frame,
                            text="🗑️ Clear History",
                            command=lambda: self.history_listbox.delete(0, tk.END),
                            font=("Segoe UI", 9),
                            bg="#FF6B6B",
                            fg="white",
                            relief="flat",
                            padx=10,
                            pady=5,
                            cursor="hand2")
        clear_btn.pack(pady=(0, 5))
    
    def create_stats_section(self):
        """Create statistics section"""
        stats_frame = tk.LabelFrame(self.right_frame,
                                   text="📈 STATISTICS",
                                   font=("Segoe UI", 12, "bold"),
                                   bg=THEME["bg"],
                                   fg=THEME["accent"],
                                   relief="flat")
        stats_frame.pack(fill="x", padx=5, pady=5)
        
        stats_content = tk.Frame(stats_frame, bg=THEME["bg"])
        stats_content.pack(fill="x", padx=10, pady=10)
        
        # Stats labels
        self.games_label = tk.Label(stats_content,
                                   text="📊 Games: 0",
                                   font=("Segoe UI", 10),
                                   bg=THEME["bg"],
                                   fg=THEME["fg"])
        self.games_label.pack(anchor="w", pady=3)
        
        self.wins_label = tk.Label(stats_content,
                                  text="🏆 Human Wins: 0",
                                  font=("Segoe UI", 10),
                                  bg=THEME["bg"],
                                  fg=THEME["fg"])
        self.wins_label.pack(anchor="w", pady=3)
        
        self.ai_wins_label = tk.Label(stats_content,
                                     text="🤖 AI Wins: 0",
                                     font=("Segoe UI", 10),
                                     bg=THEME["bg"],
                                     fg=THEME["fg"])
        self.ai_wins_label.pack(anchor="w", pady=3)
        
        self.draws_label = tk.Label(stats_content,
                                   text="🤝 Draws: 0",
                                   font=("Segoe UI", 10),
                                   bg=THEME["bg"],
                                   fg=THEME["fg"])
        self.draws_label.pack(anchor="w", pady=3)
        
        self.moves_label = tk.Label(stats_content,
                                   text="🎯 Total Moves: 0",
                                   font=("Segoe UI", 10),
                                   bg=THEME["bg"],
                                   fg=THEME["fg"])
        self.moves_label.pack(anchor="w", pady=3)
        
        # Reset button
        reset_btn = tk.Button(stats_content,
                            text="🔄 Reset Stats",
                            command=self.reset_stats,
                            font=("Segoe UI", 9),
                            bg="#95A5A6",
                            fg="white",
                            relief="flat",
                            padx=10,
                            pady=5,
                            cursor="hand2")
        reset_btn.pack(anchor="e", pady=(10, 0))
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts - REMOVED Ctrl+H (hint)"""
        self.root.bind("<Control-n>", lambda e: self.start_game())
        self.root.bind("<Control-z>", lambda e: self.undo_move())
        self.root.bind("<F1>", lambda e: self.show_help())
        self.root.bind("<Escape>", lambda e: self.root.quit())
    
    def lighten_color(self, color, factor=1.2):
        """Lighten a hex color"""
        try:
            if color.startswith("#") and len(color) == 7:
                r = min(255, int(int(color[1:3], 16) * factor))
                g = min(255, int(int(color[3:5], 16) * factor))
                b = min(255, int(int(color[5:7], 16) * factor))
                return f"#{r:02x}{g:02x}{b:02x}"
        except:
            pass
        return color
    
    def darken_color(self, color, factor=0.7):
        """Darken a hex color"""
        try:
            if color.startswith("#") and len(color) == 7:
                r = int(int(color[1:3], 16) * factor)
                g = int(int(color[3:5], 16) * factor)
                b = int(int(color[5:7], 16) * factor)
                return f"#{r:02x}{g:02x}{b:02x}"
        except:
            pass
        return color
    
    def get_brightness(self, color):
        """Get brightness of a color"""
        try:
            if color.startswith("#") and len(color) == 7:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                return (r + g + b) // 3
        except:
            pass
        return 128
    
    def on_canvas_resize(self, event):
        """Handle canvas resize"""
        if self.game_active and self.board:
            self.draw_board()
    
    def draw_board(self):
        """Draw the game board with current theme"""
        if not self.game_active or not self.board:
            return
        
        self.canvas.delete("all")
        
        # Calculate dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 10 or canvas_height <= 10:
            return
        
        available_width = canvas_width - PADDING * 2
        available_height = canvas_height - PADDING * 2
        
        # Use self.board.n for cell size calculation
        cell_size = min(available_width // self.board.n, 
                       available_height // self.board.n)
        
        if cell_size < 10:  # Minimum cell size
            cell_size = 10
        
        # Calculate total board size in pixels
        board_pixel_size = cell_size * self.board.n
        
        # Draw grid lines
        for i in range(self.board.n):
            # Horizontal lines
            y = PADDING + i * cell_size
            self.canvas.create_line(PADDING, y, 
                                   PADDING + board_pixel_size, y,
                                   fill=THEME["grid_color"], width=1)
            
            # Vertical lines
            x = PADDING + i * cell_size
            self.canvas.create_line(x, PADDING,
                                   x, PADDING + board_pixel_size,
                                   fill=THEME["grid_color"], width=1)
        
        # Draw coordinates
        for i in range(self.board.n):
            # Column numbers (top)
            x = PADDING + i * cell_size
            self.canvas.create_text(x + cell_size // 2, PADDING - 20, 
                                   text=str(i + 1),
                                   font=("Arial", 9),
                                   fill=THEME["fg"])
            
            # Row numbers (left)
            y = PADDING + i * cell_size
            self.canvas.create_text(PADDING - 20, y + cell_size // 2, 
                                   text=str(i + 1),
                                   font=("Arial", 9),
                                   fill=THEME["fg"])
        
        # Draw pieces
        for r in range(self.board.n):
            for c in range(self.board.n):
                player = self.board.grid[r][c]
                if player != 0:
                    self.draw_piece(r, c, player, cell_size)
        
        # Highlight last move
        if self.board.last_move:
            r, c = self.board.last_move
            x = PADDING + c * cell_size
            y = PADDING + r * cell_size
            
            self.canvas.create_rectangle(x-3, y-3,
                                       x+cell_size+3, y+cell_size+3,
                                       outline=THEME["highlight"],
                                       width=3,
                                       tags="highlight")
    
    def draw_piece(self, r, c, player, cell_size):
        """Draw a game piece"""
        x = PADDING + c * cell_size + cell_size // 2
        y = PADDING + r * cell_size + cell_size // 2
        
        radius = max(5, cell_size // 2 - 4)
        
        if player == AI:
            color = THEME["ai_color"]
            text = "AI"
        else:
            color = THEME["human_color"]
            text = "H"
        
        # Draw piece with shadow
        shadow_offset = 2
        self.canvas.create_oval(x-radius+shadow_offset, y-radius+shadow_offset,
                               x+radius+shadow_offset, y+radius+shadow_offset,
                               fill=self.darken_color(color, 0.7),
                               outline="",
                               tags="piece")
        
        # Main piece
        self.canvas.create_oval(x-radius, y-radius,
                               x+radius, y+radius,
                               fill=color,
                               outline=THEME["fg"],
                               width=2,
                               tags="piece")
        
        # Piece label
        text_color = "white" if self.get_brightness(color) < 128 else "black"
        self.canvas.create_text(x, y,
                               text=text,
                               fill=text_color,
                               font=("Arial", max(8, cell_size//3), "bold"),
                               tags="piece")
    
    def handle_click(self, event):
        """Handle mouse click on board"""
        if not self.game_active or not self.board or self.ai_thinking:
            return
        
        # Calculate cell size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        available_width = canvas_width - PADDING * 2
        available_height = canvas_height - PADDING * 2
        
        cell_size = min(available_width // self.board.n, 
                       available_height // self.board.n)
        
        if cell_size == 0:
            return
        
        # Convert click coordinates to grid position
        click_x = event.x - PADDING
        click_y = event.y - PADDING
        
        # Calculate column and row
        c = click_x // cell_size
        r = click_y // cell_size
        
        # Validate the position
        max_pixel = cell_size * (self.board.n - 1)
        margin = cell_size // 2
        
        if click_x < -margin or click_x > max_pixel + margin:
            return
        if click_y < -margin or click_y > max_pixel + margin:
            return
        
        # Clamp to valid grid positions
        c = max(0, min(self.board.n - 1, c))
        r = max(0, min(self.board.n - 1, r))
        
        # Check if valid move
        if not self.board.is_valid_move(r, c):
            # Show feedback for invalid move
            x = PADDING + c * cell_size + cell_size // 2
            y = PADDING + r * cell_size + cell_size // 2
            self.canvas.create_oval(x-10, y-10, x+10, y+10,
                                   outline="#FF0000",
                                   width=2,
                                   tags="invalid")
            self.root.after(1000, lambda: self.canvas.delete("invalid"))
            return
        
        # Make human move
        if self.board.current_player == HUMAN:
            self.make_human_move(r, c)
    
    def make_human_move(self, r, c):
        """Make a move for human player"""
        if not self.board.make_move(r, c, HUMAN):
            return
        
        # Add to history
        self.history_listbox.insert(tk.END, f"Human: ({r+1}, {c+1})")
        self.history_listbox.see(tk.END)
        
        self.draw_board()
        self.update_game_info()
        
        # Check for winner
        if self.board.check_winner(HUMAN):
            self.game_over("🎉 Human Wins!", "human")
            return
        
        # Check for draw
        if self.board.is_game_over():
            self.game_over("🤝 It's a Draw!", "draw")
            return
        
        # AI's turn
        self.status_label.config(text="🤖 AI is thinking...")
        self.thinking_label.config(text="Thinking...")
        self.ai_thinking = True
        self.root.update()
        
        # Make AI move
        self.root.after(100, self.make_ai_move)
    
    def make_ai_move(self):
        """Make a move for AI player"""
        if not self.game_active or not self.board:
            return
        
        start_time = time.time()
        move = self.ai_player.get_best_move(self.board)
        
        if move:
            r, c = move
            self.board.make_move(r, c, AI)
            
            move_time = time.time() - start_time
            
            # Add to history
            self.history_listbox.insert(tk.END, f"AI: ({r+1}, {c+1}) [{move_time:.2f}s]")
            self.history_listbox.see(tk.END)
            
            self.draw_board()
            self.update_game_info()
            
            # Update stats
            self.stats["total_moves"] += 1
            
            # Stop thinking indicator
            self.thinking_label.config(text="")
            self.ai_thinking = False
            
            # Check for winner
            if self.board.check_winner(AI):
                self.game_over("🤖 AI Wins!", "ai")
                return
            
            # Check for draw
            if self.board.is_game_over():
                self.game_over("🤝 It's a Draw!", "draw")
                return
            
            self.status_label.config(text="✅ Your turn!")
        else:
            self.thinking_label.config(text="")
            self.ai_thinking = False
            self.status_label.config(text="❌ AI couldn't find a move")
    
    def start_game(self):
        """Start a new game"""
        try:
            # Get settings
            board_size = int(self.size_var.get())
            difficulty = self.diff_var.get()
            first_player = self.player_var.get()
            
            # Initialize game
            self.board = Board(board_size)
            self.ai_player = AIPlayer(difficulty=difficulty, board_size=board_size)
            self.game_active = True
            self.ai_thinking = False
            
            # Clear history
            self.history_listbox.delete(0, tk.END)
            
            # Update info
            self.update_game_info()
            self.update_stats_display()
            
            # Set status
            self.status_label.config(text="✅ Game started! Click to place your stone.")
            
            # Draw board
            self.draw_board()
            
            # Update stats
            self.stats["games"] += 1
            
            # If AI goes first
            if first_player == "AI":
                self.status_label.config(text="🤖 AI is thinking...")
                self.thinking_label.config(text="Thinking...")
                self.ai_thinking = True
                self.root.update()
                self.root.after(500, self.make_ai_move)
            
            print(f"\n🎮 New game started:")
            print(f"  Board: {board_size}x{board_size}")
            print(f"  Difficulty: {difficulty}")
            print(f"  First player: {first_player}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start game: {str(e)}")
            print(f"❌ Error starting game: {e}")
    
    def undo_move(self):
        """Undo the last move"""
        if not self.game_active or not self.board or not self.board.move_history:
            messagebox.showinfo("Info", "No moves to undo!")
            return
        
        if self.board.undo_move():
            # Remove from history
            if self.history_listbox.size() > 0:
                self.history_listbox.delete(tk.END)
            
            self.draw_board()
            self.update_game_info()
            
            # Stop AI thinking
            if self.ai_thinking:
                self.thinking_label.config(text="")
                self.ai_thinking = False
            
            self.status_label.config(text="↩️ Move undone!")
    
    def restart_game(self):
        """Restart the current game"""
        if messagebox.askyesno("Restart Game", "Are you sure you want to restart?"):
            self.start_game()
    
    def show_help(self):
        """Show help dialog - REMOVED hint reference"""
        help_text = """
🎮 HOW TO PLAY GOMOKU

OBJECTIVE:
Be the first to place 5 stones in a row 
(horizontally, vertically, or diagonally).

CONTROLS:
• Click on any empty intersection to place your stone
• Ctrl+Z: Undo last move
• Ctrl+N: New game
• F1: Show this help

DIFFICULTY LEVELS:
• Easy: Mostly random moves (80% random)
• Medium: Balanced strategy (20% random)
• Hard: Advanced strategy (no random moves)
• Adaptive: Adjusts difficulty based on game state

TIPS:
1. Control the center of the board
2. Create multiple threats at once
3. Block your opponent's potential lines

GOOD LUCK! 🍀
        """
        messagebox.showinfo("How to Play", help_text)
    
    def reset_stats(self):
        """Reset game statistics"""
        if messagebox.askyesno("Reset Statistics", "Reset all statistics?"):
            self.stats = {
                "games": 0,
                "human_wins": 0,
                "ai_wins": 0,
                "draws": 0,
                "total_moves": 0
            }
            self.update_stats_display()
    
    def game_over(self, message, winner):
        """Handle game over"""
        self.game_active = False
        self.thinking_label.config(text="")
        self.ai_thinking = False
        if winner == "human":
            self.stats["human_wins"] += 1
        elif winner == "ai":
            self.stats["ai_wins"] += 1
        else:
            self.stats["draws"] += 1
        
        self.update_stats_display()
        self.status_label.config(text=message)
        self.root.after(1000, self.ask_play_again)
    
    def ask_play_again(self):
        """Ask if player wants to play again"""
        response = messagebox.askyesno("Game Over", "Play again?")
        if response:
            self.start_game()
    
    def update_game_info(self):
        """Update game information display"""
        if not self.board:
            return
        
        player = "Human" if self.board.current_player == HUMAN else "AI"
        self.player_info.config(text=f"Current Player: {player}")
        self.move_count_info.config(text=f"Moves: {self.board.move_count}")
        status = "In Progress" if self.game_active else "Game Over"
        self.game_status_info.config(text=f"Status: {status}")
        self.board_info.config(text=f"Board: {self.board.n}×{self.board.n}")
        self.diff_info.config(text=f"Difficulty: {self.diff_var.get()}")
    
    def update_stats_display(self):
        """Update statistics display"""
        self.games_label.config(text=f"📊 Games: {self.stats['games']}")
        self.wins_label.config(text=f"🏆 Human Wins: {self.stats['human_wins']}")
        self.ai_wins_label.config(text=f"🤖 AI Wins: {self.stats['ai_wins']}")
        self.draws_label.config(text=f"🤝 Draws: {self.stats['draws']}")
        self.moves_label.config(text=f"🎯 Total Moves: {self.stats['total_moves']}")

def main():
    """Main function to start the application"""
    root = tk.Tk()
    app = ModernGomokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()