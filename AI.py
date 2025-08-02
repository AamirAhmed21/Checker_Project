# ai.py

import threading
import time
import random
from tkinter import messagebox
from PiecesState import PiecesState
from Pieces import Pieces
# from CheckersBoard import CheckersBoard  # Removed to avoid circular import
from PiecesMove import PiecesMove


class AI(threading.Thread):
    SEARCH_DEPTH = 3
    MAX_VALUE = 999999
    MIN_VALUE = -999999
    DIFFICULTY = "medium"  # easy, medium, hard

    def __init__(self):
        super().__init__()
        self.current_state = None
        self.possible_next_states = None
        self.game_board = None
        self.daemon = True
        self.start()

    def set_state(self, state):
        self.current_state = state

    def run(self):
        while True:
            try:
                time.sleep(0.1)
                if self.current_state is not None and self.game_board and not self.game_board.is_player_turn:
                    self.alpha_beta_search(self.current_state)
            except Exception as e:
                print(f"AI thread error: {e}")
                time.sleep(0.1)

    def set_difficulty(self, difficulty):
        """Set AI difficulty level"""
        self.DIFFICULTY = difficulty
        if difficulty == "easy":
            self.SEARCH_DEPTH = 1
        elif difficulty == "medium":
            self.SEARCH_DEPTH = 3
        elif difficulty == "hard":
            self.SEARCH_DEPTH = 5

    def alpha_beta_search(self, state):
        print("AI starting move calculation...")
        
        if self.DIFFICULTY == "easy":
            self.easy_ai_move(state)
        elif self.DIFFICULTY == "medium":
            self.medium_ai_move(state)
        elif self.DIFFICULTY == "hard":
            self.hard_ai_move(state)

    def easy_ai_move(self, state):
        """Easy AI: Simple moves with basic capture awareness"""
        print("Easy AI making move...")
        red_pieces = []
        for i in range(12):
            if state.current_red_pieces[i].is_visible():
                red_pieces.append(state.current_red_pieces[i])
        
        if not red_pieces:
            print("No red pieces available for AI")
            return
        
        # Find all possible moves
        capture_moves = []
        regular_moves = []
        
        for piece in red_pieces:
            current_pos = piece.get_location()
            
            # Check regular moves
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    new_x = current_pos[0] + dx * 60
                    new_y = current_pos[1] + dy * 60
                    if 0 <= new_x < 480 and 0 <= new_y < 480:
                        if self.is_valid_move(piece, (new_x, new_y), state):
                            regular_moves.append((piece, (new_x, new_y)))
            
            # Check capture moves
            for dx in [-2, 2]:
                for dy in [-2, 2]:
                    new_x = current_pos[0] + dx * 60
                    new_y = current_pos[1] + dy * 60
                    if 0 <= new_x < 480 and 0 <= new_y < 480:
                        if self.is_valid_capture_move(piece, (new_x, new_y), state):
                            capture_moves.append((piece, (new_x, new_y)))
        
        # Prioritize captures but choose randomly
        if capture_moves:
            piece, move = random.choice(capture_moves)
            print(f"Easy AI capturing from {piece.get_location()} to {move}")
            self.perform_capture(piece, move, state)
        elif regular_moves:
            piece, move = random.choice(regular_moves)
            print(f"Easy AI moving from {piece.get_location()} to {move}")
            piece.set_location(move)
            self.update_board(state)
        else:
            print("Easy AI couldn't find a valid move")

    def medium_ai_move(self, state):
        """Medium AI: Prioritize captures and strategic moves"""
        print("Medium AI making move...")
        red_pieces = []
        for i in range(12):
            if state.current_red_pieces[i].is_visible():
                red_pieces.append(state.current_red_pieces[i])
        
        if not red_pieces:
            print("No red pieces available for AI")
            return
        
        # Find all possible moves
        capture_moves = []
        regular_moves = []
        
        for piece in red_pieces:
            current_pos = piece.get_location()
            
            # Check regular moves
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    new_x = current_pos[0] + dx * 60
                    new_y = current_pos[1] + dy * 60
                    if 0 <= new_x < 480 and 0 <= new_y < 480:
                        if self.is_valid_move(piece, (new_x, new_y), state):
                            regular_moves.append((piece, (new_x, new_y)))
            
            # Check capture moves
            for dx in [-2, 2]:
                for dy in [-2, 2]:
                    new_x = current_pos[0] + dx * 60
                    new_y = current_pos[1] + dy * 60
                    if 0 <= new_x < 480 and 0 <= new_y < 480:
                        if self.is_valid_capture_move(piece, (new_x, new_y), state):
                            capture_moves.append((piece, (new_x, new_y)))
        
        print(f"Found {len(capture_moves)} capture moves and {len(regular_moves)} regular moves")
        
        # Prioritize captures
        if capture_moves:
            # Choose the best capture move (prefer moves that get closer to promotion)
            best_capture = None
            best_score = -1
            
            for piece, move in capture_moves:
                score = self.evaluate_move(piece, move, state)
                if score > best_score:
                    best_score = score
                    best_capture = (piece, move)
            
            piece, move = best_capture
            print(f"Medium AI capturing from {piece.get_location()} to {move}")
            # Perform the capture
            self.perform_capture(piece, move, state)
            # Check for additional jumps
            self.perform_additional_jumps(piece, state)
        elif regular_moves:
            # Choose the best regular move
            best_move = None
            best_score = -1
            
            for piece, move in regular_moves:
                score = self.evaluate_move(piece, move, state)
                if score > best_score:
                    best_score = score
                    best_move = (piece, move)
            
            piece, move = best_move
            print(f"Medium AI moving from {piece.get_location()} to {move}")
            piece.set_location(move)
            self.update_board(state)
        else:
            print("Medium AI couldn't find a valid move")

    def perform_capture(self, piece, move, state):
        """Perform a capture move and remove the captured piece"""
        current_pos = piece.get_location()
        piece.set_location(move)
        
        # Find and remove the captured piece
        middle_x = current_pos[0] + (move[0] - current_pos[0]) // 2
        middle_y = current_pos[1] + (move[1] - current_pos[1]) // 2
        
        for i in range(12):
            if (state.current_white_pieces[i].is_visible() and 
                state.current_white_pieces[i].get_location() == (middle_x, middle_y)):
                state.current_white_pieces[i].set_visible(False)
                print(f"AI captured white piece at ({middle_x}, {middle_y})")
                break
        
        self.update_board(state)

    def perform_additional_jumps(self, piece, state):
        """Perform additional jumps if available"""
        max_jumps = 10  # Prevent infinite loops
        jump_count = 0
        
        while jump_count < max_jumps:
            additional_jumps = []
            current_pos = piece.get_location()
            
            # Check for additional capture moves
            for dx in [-2, 2]:
                for dy in [-2, 2]:
                    new_x = current_pos[0] + dx * 60
                    new_y = current_pos[1] + dy * 60
                    if 0 <= new_x < 480 and 0 <= new_y < 480:
                        if self.is_valid_capture_move(piece, (new_x, new_y), state):
                            additional_jumps.append((new_x, new_y))
            
            if additional_jumps:
                # Choose a random additional jump
                next_move = random.choice(additional_jumps)
                print(f"AI continuing jump to {next_move}")
                self.perform_capture(piece, next_move, state)
                jump_count += 1
                time.sleep(0.2)  # Small delay to show the jumps
            else:
                break
        
        if jump_count > 0:
            print(f"AI completed {jump_count} additional jumps")

    def hard_ai_move(self, state):
        """Hard AI: Strategic moves with evaluation"""
        print("Hard AI making move...")
        red_pieces = []
        for i in range(12):
            if state.current_red_pieces[i].is_visible():
                red_pieces.append(state.current_red_pieces[i])
        
        if not red_pieces:
            print("No red pieces available for AI")
            return
        
        best_move = None
        best_score = float('-inf')
        
        # Evaluate all possible moves
        for piece in red_pieces:
            current_pos = piece.get_location()
            
            # Check all possible moves for this piece
            for dx in [-2, -1, 1, 2]:
                for dy in [-2, -1, 1, 2]:
                    if abs(dx) == abs(dy):  # Diagonal moves only
                        new_x = current_pos[0] + dx * 60
                        new_y = current_pos[1] + dy * 60
                        
                        if 0 <= new_x < 480 and 0 <= new_y < 480:
                            if self.is_valid_move(piece, (new_x, new_y), state):
                                # Evaluate this move
                                score = self.evaluate_move(piece, (new_x, new_y), state)
                                if score > best_score:
                                    best_score = score
                                    best_move = (piece, (new_x, new_y))
        
        if best_move:
            piece, move = best_move
            print(f"Hard AI making strategic move from {piece.get_location()} to {move}")
            
            # Check if it's a capture move
            if self.is_valid_capture_move(piece, move, state):
                self.perform_capture(piece, move, state)
                self.perform_additional_jumps(piece, state)
            else:
                piece.set_location(move)
                self.update_board(state)
        else:
            print("Hard AI couldn't find a valid move")

    def is_valid_move(self, piece, move, state):
        """Check if a move is valid"""
        current_pos = piece.get_location()
        dx = move[0] - current_pos[0]
        dy = move[1] - current_pos[1]
        
        # Must be diagonal move
        if abs(dx) != abs(dy):
            return False
        
        # Check if destination is empty
        for i in range(12):
            if (state.current_red_pieces[i].is_visible() and 
                state.current_red_pieces[i].get_location() == move):
                return False
            if (state.current_white_pieces[i].is_visible() and 
                state.current_white_pieces[i].get_location() == move):
                return False
        
        # For regular pieces, check direction
        if not piece.is_king():
            if piece.get_color() == "red" and dy > 0:  # Red pieces move down
                return True
            elif piece.get_color() == "white" and dy < 0:  # White pieces move up
                return True
            return False
        
        return True

    def is_valid_capture_move(self, piece, move, state):
        """Check if a capture move is valid"""
        current_pos = piece.get_location()
        dx = move[0] - current_pos[0]
        dy = move[1] - current_pos[1]
        
        # Must be a jump (distance 2)
        if abs(dx) != 2 or abs(dy) != 2:
            return False
        
        # Check if destination is empty
        for i in range(12):
            if (state.current_red_pieces[i].is_visible() and 
                state.current_red_pieces[i].get_location() == move):
                return False
            if (state.current_white_pieces[i].is_visible() and 
                state.current_white_pieces[i].get_location() == move):
                return False
        
        # Check if there's an opponent piece in the middle
        middle_x = current_pos[0] + (dx // 2)
        middle_y = current_pos[1] + (dy // 2)
        
        # Check for opponent piece in the middle
        for i in range(12):
            if (state.current_white_pieces[i].is_visible() and 
                state.current_white_pieces[i].get_location() == (middle_x, middle_y) and
                piece.get_color() == "red"):
                return True
            if (state.current_red_pieces[i].is_visible() and 
                state.current_red_pieces[i].get_location() == (middle_x, middle_y) and
                piece.get_color() == "white"):
                return True
        
        return False

    def evaluate_move(self, piece, move, state):
        """Evaluate the strategic value of a move"""
        score = 0
        current_pos = piece.get_location()
        
        # Bonus for captures
        if self.is_valid_capture_move(piece, move, state):
            score += 50  # High priority for captures
        
        # Bonus for moving towards promotion (getting closer to bottom)
        if piece.get_color() == "red" and move[1] > current_pos[1]:
            score += 5
            # Extra bonus for getting very close to promotion
            if move[1] >= 420:  # Very close to bottom
                score += 10
        
        # Bonus for king moves (kings are more valuable)
        if piece.is_king():
            score += 3
        
        # Bonus for moving to center positions (more strategic)
        center_x, center_y = 240, 240
        distance_to_center = abs(move[0] - center_x) + abs(move[1] - center_y)
        score += (480 - distance_to_center) / 50
        
        # Bonus for moving to edges (safer positions)
        if move[0] == 0 or move[0] == 420 or move[1] == 0 or move[1] == 420:
            score += 2
        
        # Penalty for moving backwards (for regular pieces)
        if not piece.is_king() and piece.get_color() == "red" and move[1] < current_pos[1]:
            score -= 5
        
        return score

    def update_board(self, state):
        """Update the game board after AI move"""
        if self.game_board:
            self.game_board.red_pieces = state.current_red_pieces
            self.game_board.white_pieces = state.current_white_pieces
            self.game_board.paint()
            
            # Check for win conditions after AI move
            self.game_board.check_win_conditions()
            
            self.game_board.is_player_turn = True
            print("AI move completed")

    def set_board(self, board):
        self.game_board = board

    def check_over(self, state):
        red_pieces = state.current_red_pieces
        white_pieces = state.current_white_pieces

        for i in range(12):
            if red_pieces[i].is_visible():
                break
            if i == 11:
                messagebox.showinfo("Game Over", "You Won!")
                return

        for i in range(12):
            if white_pieces[i].is_visible():
                break
            if i == 11:
                messagebox.showinfo("Game Over", "You Lost!")
                return
