# checkers_board.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Pieces import Pieces
# from AI import AI  # Removed to avoid circular import
# from PiecesState import PiecesState  # Will import inside function to avoid circular import
from PiecesMove import PiecesMove


class CheckersBoard(tk.Canvas):
    selected_pieces = None
    ai = None
    monster = None
    pieces_state = None
    must_capture = False  # New: track if capture is mandatory
    current_jumper = None  # New: track piece that must continue jumping

    white_pieces = [None] * 12
    red_pieces = [None] * 12
    board_points = [[None for _ in range(9)] for _ in range(9)]
    is_player_turn = True

    # Load images (static)
    red_checkers_image = None
    white_checkers_image = None
    red_king_image = None
    white_king_image = None
    background_image = None

    def __init__(self, master, ai_instance):
        super().__init__(master, width=480, height=480, bg="white")
        self.ai = ai_instance
        self.init_board()
        self.load_images()
        self.paint()  # Initial paint
        self.bind("<Button-1>", self.mouse_pressed)

    def init_board(self):
        for i in range(1, 9):
            for j in range(1, 9):
                self.board_points[i][j] = (60 * (i - 1), 60 * (j - 1))

        for i in range(12):
            self.red_pieces[i] = Pieces("red", i)
            self.white_pieces[i] = Pieces("white", i)

        for i in range(4):
            self.red_pieces[i].set_location(self.board_points[2 * i + 2][1])
        for i in range(4, 8):
            self.red_pieces[i].set_location(self.board_points[2 * (i - 4) + 1][2])
        for i in range(8, 12):
            self.red_pieces[i].set_location(self.board_points[2 * (i - 8) + 2][3])

        for i in range(4):
            self.white_pieces[i].set_location(self.board_points[2 * i + 1][6])
        for i in range(4, 8):
            self.white_pieces[i].set_location(self.board_points[2 * (i - 4) + 2][7])
        for i in range(8, 12):
            self.white_pieces[i].set_location(self.board_points[2 * (i - 8) + 1][8])

        self.is_player_turn = True

    def load_images(self):
        self.red_checkers_image = ImageTk.PhotoImage(Image.open("resources/redCheckers.png").resize((60, 60)))
        self.white_checkers_image = ImageTk.PhotoImage(Image.open("resources/whiteCheckers.png").resize((60, 60)))
        self.red_king_image = ImageTk.PhotoImage(Image.open("resources/redKing.png").resize((60, 60)))
        self.white_king_image = ImageTk.PhotoImage(Image.open("resources/whiteKing.png").resize((60, 60)))
        self.background_image = ImageTk.PhotoImage(Image.open("resources/backGround.jpg").resize((480, 480)))

    def paint(self):
        try:
            self.delete("all")  # Clear the canvas first
            self.create_image(0, 0, image=self.background_image, anchor=tk.NW)

            for i in range(12):
                if self.red_pieces[i].is_visible():
                    x, y = self.red_pieces[i].get_location()
                    if self.red_pieces[i].is_king():
                        self.create_image(x, y, image=self.red_king_image, anchor=tk.NW)
                    else:
                        self.create_image(x, y, image=self.red_checkers_image, anchor=tk.NW)

                if self.white_pieces[i].is_visible():
                    x, y = self.white_pieces[i].get_location()
                    if self.white_pieces[i].is_king():
                        self.create_image(x, y, image=self.white_king_image, anchor=tk.NW)
                    else:
                        self.create_image(x, y, image=self.white_checkers_image, anchor=tk.NW)
        except Exception as e:
            print(f"Error in paint method: {e}")
            # Fallback to simple drawing if images fail
            self.delete("all")
            # Draw simple background
            for i in range(8):
                for j in range(8):
                    x, y = i * 60, j * 60
                    color = "white" if (i + j) % 2 == 0 else "gray"
                    self.create_rectangle(x, y, x + 60, y + 60, fill=color, outline="black")
            
            # Draw pieces as circles
            for i in range(12):
                if self.red_pieces[i].is_visible():
                    x, y = self.red_pieces[i].get_location()
                    self.create_oval(x + 5, y + 5, x + 55, y + 55, fill="red", outline="darkred", width=2)
                    if self.red_pieces[i].is_king():
                        self.create_text(x + 30, y + 30, text="K", fill="white", font=("Arial", 16, "bold"))

                if self.white_pieces[i].is_visible():
                    x, y = self.white_pieces[i].get_location()
                    self.create_oval(x + 5, y + 5, x + 55, y + 55, fill="white", outline="gray", width=2)
                    if self.white_pieces[i].is_king():
                        self.create_text(x + 30, y + 30, text="K", fill="black", font=("Arial", 16, "bold"))

    def mouse_pressed(self, event):
        if PiecesMove.has_winner:
            return

        if not self.is_player_turn:
            messagebox.showinfo("Info", "AI is thinking, please wait...")
            return

        x, y = event.x, event.y

        if self.pieces_state and len(self.pieces_state.next_states_of_white()) == 0:
            messagebox.showinfo("Game Over", "You Lost!")
            return

        # Check for mandatory captures at the start of player's turn
        if not self.current_jumper:
            self.check_for_mandatory_captures()

        selected_point = self.get_point(x, y)

        # Check if clicking on red pieces (not allowed)
        for i in range(12):
            if self.red_pieces[i].is_visible() and self.red_pieces[i].get_location() == selected_point:
                return

        # Clear previous selections
        for i in range(12):
            self.white_pieces[i].set_selected(False)

        # Handle piece selection
        for i in range(12):
            if self.white_pieces[i].is_visible() and self.white_pieces[i].get_location() == selected_point:
                # Check if we must continue jumping with the same piece
                if self.current_jumper and self.white_pieces[i] != self.current_jumper:
                    messagebox.showinfo("Invalid Selection", "You must continue jumping with the same piece!")
                    return
                
                self.selected_pieces = self.white_pieces[i]
                self.white_pieces[i].set_selected(True)
                self.paint()
                return

        # Handle move execution
        if self.selected_pieces:
            former_point = self.selected_pieces.get_location()
            if self.judging_move(self.selected_pieces, former_point, selected_point):
                self.selected_pieces.set_location(selected_point)

                # Check for king promotion
                for i in range(1, 9):
                    if self.selected_pieces.get_color() == "white" and selected_point == self.board_points[i][1]:
                        self.selected_pieces.set_king(True)
                        self.selected_pieces.set_visible(True)

                self.paint()

                # Check for additional jumps
                if self.monster and self.monster == self.selected_pieces:
                    self.current_jumper = self.selected_pieces
                    additional_jumps = self.get_additional_jumps(self.selected_pieces)
                    if additional_jumps:
                        messagebox.showinfo("Continue Jumping", "You must continue jumping with the same piece!")
                        self.selected_pieces = None
                        return
                    else:
                        self.current_jumper = None
                        self.monster = None
                        self.must_capture = False
                        # End turn and let AI play
                        self.end_player_turn()
                else:
                    # Regular move - check if captures were available
                    if self.must_capture:
                        messagebox.showinfo("Invalid Move", "You must capture if possible!")
                        self.selected_pieces.set_location(former_point)  # Undo move
                        self.paint()
                        return
                    else:
                        self.end_player_turn()

    def get_additional_jumps(self, piece):
        """Check if the piece can make additional jumps after a capture"""
        jumps = []
        current_pos = piece.get_location()
        
        # Check all diagonal directions for additional captures
        for dx in [-2, 2]:
            for dy in [-2, 2]:
                new_x = current_pos[0] + dx * 60
                new_y = current_pos[1] + dy * 60
                
                if 0 <= new_x < 480 and 0 <= new_y < 480:
                    # Check if destination is empty
                    dest_occupied = False
                    for i in range(12):
                        if (self.red_pieces[i].is_visible() and 
                            self.red_pieces[i].get_location() == (new_x, new_y)):
                            dest_occupied = True
                            break
                        if (self.white_pieces[i].is_visible() and 
                            self.white_pieces[i].get_location() == (new_x, new_y)):
                            dest_occupied = True
                            break
                    
                    if not dest_occupied:
                        # Check if there's an opponent piece in the middle
                        middle_x = current_pos[0] + (dx // 2) * 60
                        middle_y = current_pos[1] + (dy // 2) * 60
                        
                        for i in range(12):
                            if (self.red_pieces[i].is_visible() and 
                                self.red_pieces[i].get_location() == (middle_x, middle_y)):
                                jumps.append((new_x, new_y))
                                break
        
        return jumps

    def end_player_turn(self):
        """End the player's turn and start AI turn"""
        if self.selected_pieces.get_color() == "white":
            # Check for win conditions before ending turn
            self.check_win_conditions()
            
            from PiecesState import PiecesState
            state = PiecesState(self.red_pieces, self.white_pieces, True)
            self.ai.set_state(state)
            self.ai.set_board(self)
            # Don't start the thread again, it's already running
            self.selected_pieces = None
            self.is_player_turn = False

    def check_win_conditions(self):
        """Check if the game is over due to win conditions"""
        # Count visible pieces
        red_count = 0
        white_count = 0
        
        for i in range(12):
            if self.red_pieces[i].is_visible():
                red_count += 1
            if self.white_pieces[i].is_visible():
                white_count += 1
        
        # Check if all red pieces are captured (player wins)
        if red_count == 0:
            messagebox.showinfo("Game Over", "You Win! All red pieces captured!")
            PiecesMove.has_winner = True
            return True
        
        # Check if all white pieces are captured (AI wins)
        if white_count == 0:
            messagebox.showinfo("Game Over", "You Lose! All white pieces captured!")
            PiecesMove.has_winner = True
            return True
        
        # Check if player has no valid moves
        if not self.has_valid_moves("white"):
            messagebox.showinfo("Game Over", "You Lose! No valid moves available!")
            PiecesMove.has_winner = True
            return True
        
        # Check if AI has no valid moves
        if not self.has_valid_moves("red"):
            messagebox.showinfo("Game Over", "You Win! AI has no valid moves!")
            PiecesMove.has_winner = True
            return True
        
        return False

    def has_valid_moves(self, color):
        """Check if the specified color has any valid moves"""
        pieces = self.white_pieces if color == "white" else self.red_pieces
        
        for piece in pieces:
            if piece.is_visible():
                current_pos = piece.get_location()
                
                # Check regular moves
                for dx in [-1, 1]:
                    for dy in [-1, 1]:
                        new_x = current_pos[0] + dx * 60
                        new_y = current_pos[1] + dy * 60
                        if 0 <= new_x < 480 and 0 <= new_y < 480:
                            # Check if destination is empty
                            dest_occupied = False
                            for i in range(12):
                                if (self.red_pieces[i].is_visible() and 
                                    self.red_pieces[i].get_location() == (new_x, new_y)):
                                    dest_occupied = True
                                    break
                                if (self.white_pieces[i].is_visible() and 
                                    self.white_pieces[i].get_location() == (new_x, new_y)):
                                    dest_occupied = True
                                    break
                            
                            if not dest_occupied:
                                return True
                
                # Check capture moves
                for dx in [-2, 2]:
                    for dy in [-2, 2]:
                        new_x = current_pos[0] + dx * 60
                        new_y = current_pos[1] + dy * 60
                        if 0 <= new_x < 480 and 0 <= new_y < 480:
                            # Check if destination is empty
                            dest_occupied = False
                            for i in range(12):
                                if (self.red_pieces[i].is_visible() and 
                                    self.red_pieces[i].get_location() == (new_x, new_y)):
                                    dest_occupied = True
                                    break
                                if (self.white_pieces[i].is_visible() and 
                                    self.white_pieces[i].get_location() == (new_x, new_y)):
                                    dest_occupied = True
                                    break
                            
                            if not dest_occupied:
                                # Check if there's an opponent piece in the middle
                                middle_x = current_pos[0] + (dx // 2)
                                middle_y = current_pos[1] + (dy // 2)
                                
                                opponent_color = "white" if piece.get_color() == "red" else "red"
                                for i in range(12):
                                    if (self.white_pieces[i].is_visible() and 
                                        self.white_pieces[i].get_location() == (middle_x, middle_y) and
                                        piece.get_color() == "red"):
                                        return True
                                    if (self.red_pieces[i].is_visible() and 
                                        self.red_pieces[i].get_location() == (middle_x, middle_y) and
                                        piece.get_color() == "white"):
                                        return True
        
        return False

    def judging_move(self, piece, former, now):
        from_x, from_y, to_x, to_y = 0, 0, 0, 0
        self.monster = None

        # Find the coordinates
        for i in range(1, 9):
            for j in range(1, 9):
                if self.board_points[i][j] == former:
                    from_x, from_y = i, j
                if self.board_points[i][j] == now:
                    to_x, to_y = i, j

        # Check if destination is empty
        for i in range(12):
            if self.red_pieces[i].is_visible() and self.red_pieces[i].get_location() == now:
                return False
            if self.white_pieces[i].is_visible() and self.white_pieces[i].get_location() == now:
                return False

        # Check for mandatory captures first
        if self.must_capture:
            # Only allow capture moves
            if abs(from_x - to_x) != 2 or abs(from_y - to_y) != 2:
                return False

        # Regular moves (non-capture)
        if piece.get_color() == "white":
            # White pieces move upward (decreasing y)
            if abs(from_x - to_x) == 1 and from_y - to_y == 1:
                return True
            elif piece.is_king() and abs(from_x - to_x) == 1 and abs(from_y - to_y) == 1:
                return True

        # Capture moves
        if abs(from_x - to_x) == 2 and abs(from_y - to_y) == 2:
            # Calculate the middle position
            middle_x = (from_x + to_x) // 2
            middle_y = (from_y + to_y) // 2
            middle_pos = self.board_points[middle_x][middle_y]
            
            # Check if there's an opponent piece in the middle
            for i in range(12):
                if (self.red_pieces[i].is_visible() and 
                    self.red_pieces[i].get_location() == middle_pos):
                    # Valid capture
                    self.red_pieces[i].set_visible(False)
                    self.monster = piece
                    return True
                    
        return False

    def get_point(self, x, y):
        i, j = 1, 1
        while x - i * 60 >= 5 and i < 8:
            i += 1
        while y - j * 60 >= 5 and j < 8:
            j += 1
        return self.board_points[i][j]

    def check_for_mandatory_captures(self):
        """Check if any white pieces must capture"""
        for i in range(12):
            if self.white_pieces[i].is_visible():
                piece = self.white_pieces[i]
                current_pos = piece.get_location()
                
                # Check all possible capture directions
                for dx in [-2, 2]:
                    for dy in [-2, 2]:
                        new_x = current_pos[0] + dx * 60
                        new_y = current_pos[1] + dy * 60
                        
                        if 0 <= new_x < 480 and 0 <= new_y < 480:
                            # Check if destination is empty
                            dest_occupied = False
                            for j in range(12):
                                if (self.red_pieces[j].is_visible() and 
                                    self.red_pieces[j].get_location() == (new_x, new_y)):
                                    dest_occupied = True
                                    break
                                if (self.white_pieces[j].is_visible() and 
                                    self.white_pieces[j].get_location() == (new_x, new_y)):
                                    dest_occupied = True
                                    break
                            
                            if not dest_occupied:
                                # Check if there's an opponent piece in the middle
                                middle_x = current_pos[0] + (dx // 2) * 60
                                middle_y = current_pos[1] + (dy // 2) * 60
                                
                                for j in range(12):
                                    if (self.red_pieces[j].is_visible() and 
                                        self.red_pieces[j].get_location() == (middle_x, middle_y)):
                                        self.must_capture = True
                                        return True
        
        self.must_capture = False
        return False
