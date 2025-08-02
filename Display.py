# display.py

import tkinter as tk
from tkinter import messagebox
from AI import AI
from CheckersBoard import CheckersBoard
from PiecesMove import PiecesMove


class Display(tk.Tk):
    def __init__(self):
        super().__init__()
        self.checkers_board = None
        self.ai = None
        self.difficulty = "medium"

    def show_difficulty_menu(self):
        """Show difficulty selection dialog"""
        difficulty_window = tk.Toplevel(self)
        difficulty_window.title("Select AI Difficulty")
        difficulty_window.geometry("300x200")
        difficulty_window.resizable(False, False)
        difficulty_window.transient(self)
        difficulty_window.grab_set()
        
        # Center the window
        difficulty_window.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))
        
        # Title
        title_label = tk.Label(difficulty_window, text="Select AI Difficulty", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Difficulty buttons
        def set_difficulty(level):
            self.difficulty = level
            self.ai.set_difficulty(level)
            difficulty_window.destroy()
            self.start_game()
        
        easy_btn = tk.Button(difficulty_window, text="Easy", width=20, height=2,
                            command=lambda: set_difficulty("easy"))
        easy_btn.pack(pady=5)
        
        medium_btn = tk.Button(difficulty_window, text="Medium", width=20, height=2,
                              command=lambda: set_difficulty("medium"))
        medium_btn.pack(pady=5)
        
        hard_btn = tk.Button(difficulty_window, text="Hard", width=20, height=2,
                            command=lambda: set_difficulty("hard"))
        hard_btn.pack(pady=5)

    def start(self):
        # Setup main window
        self.title("Checkers - AI Difficulty: Medium")
        self.geometry("470x520+450+170")  # Increased height to accommodate button
        self.resizable(False, False)

        # Initialize board points for PiecesMove
        from PiecesMove import PiecesMove
        PiecesMove.init_board_points()

        # Initialize AI opponent
        self.ai = AI()
        self.ai.set_difficulty("medium")  # Default to medium
        
        # Configure grid weights for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create game board
        self.checkers_board = CheckersBoard(self, self.ai)
        self.checkers_board.grid(row=0, column=0, sticky="nsew")
        
        # Add difficulty change button at the bottom
        self.create_difficulty_button()
        
        # Show welcome message
        messagebox.showinfo("Welcome", "Checkers Game Started!\n\nYou play as White (bottom)\nAI plays as Red (top)\n\nUse the 'Change Difficulty' button to adjust AI difficulty.")
        
        # Make window visible
        self.mainloop()

    def create_difficulty_button(self):
        """Create a button to change difficulty"""
        def change_difficulty():
            current = self.ai.DIFFICULTY
            if current == "easy":
                self.ai.set_difficulty("medium")
                self.title("Checkers - AI Difficulty: Medium")
            elif current == "medium":
                self.ai.set_difficulty("hard")
                self.title("Checkers - AI Difficulty: Hard")
            else:
                self.ai.set_difficulty("easy")
                self.title("Checkers - AI Difficulty: Easy")
            
            messagebox.showinfo("Difficulty Changed", f"AI Difficulty set to: {self.ai.DIFFICULTY.capitalize()}")
        
        # Create the button directly in the main window using grid
        difficulty_btn = tk.Button(self, text="Change Difficulty", 
                                 command=change_difficulty, 
                                 bg="orange", fg="black", 
                                 font=("Arial", 14, "bold"),
                                 width=20, height=2,
                                 relief="raised",
                                 bd=3)
        difficulty_btn.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        


    def start_game(self):
        """Start the actual game after difficulty selection"""
        # Create game board
        self.checkers_board = CheckersBoard(self, self.ai)
        self.checkers_board.pack(fill="both", expand=True)
        
        # Show current difficulty
        messagebox.showinfo("Game Started", f"AI Difficulty: {self.difficulty.capitalize()}\n\nYou play as White (bottom)\nAI plays as Red (top)")
        
        # Make window visible
        self.mainloop()

    def restart(self):
        PiecesMove.has_winner = False
        self.checkers_board.init_board()
        self.checkers_board.paint()
        self.checkers_board.pack(fill="both", expand=True)

    def action_performed(self, event=None):
        # Placeholder for future button/menu actions
        pass
